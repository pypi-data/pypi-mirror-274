# ---------------------------------------------------------------------
# Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
from __future__ import annotations

import os
from pathlib import Path
from typing import List, Mapping, Optional, Tuple

import numpy as np
import qai_hub as hub
import torch
from qai_hub.public_rest_api import DatasetEntries

from qai_hub_models.models.protocols import ExecutableModelProtocol
from qai_hub_models.utils.asset_loaders import ModelZooAssetConfig, qaihm_temp_dir
from qai_hub_models.utils.base_model import BaseModel, SourceModelFormat, TargetRuntime
from qai_hub_models.utils.input_spec import InputSpec
from qai_hub_models.utils.qai_hub_helpers import (
    transpose_channel_first_to_last,
    transpose_channel_last_to_first,
)
from qai_hub_models.utils.qnn_helpers import is_qnn_hub_model

try:
    from qai_hub_models.utils.quantization_aimet import AIMETQuantizableMixin
except NotImplementedError:
    AIMETQuantizableMixin = None  # type: ignore


def prepare_compile_zoo_model_to_hub(
    model: BaseModel,
    source_model_format: SourceModelFormat,
    target_runtime: TargetRuntime,
    output_path: str | Path = "",
    input_spec: InputSpec | None = None,
    check_trace: bool = True,
    prepare_compile_options_only: bool = False,
    external_onnx_weights: bool = False,
    output_names: Optional[List[str]] = None,
) -> Tuple[str | None, str]:
    """
    Args:

    - (source_model_format, target_runtime):  One of the followings

        (1) (ONNX, QNN)

            (a) For fp32 model, torch -> onnx -> qnn.

            (b) For AIMET, torch -> onnx + aimet encodings -> qnn

        (2) (ONNX, TFLITE)

            (a) For fp32, torch (fp32) -> onnx -> tflite,

            (b) For quantized, torch(AIMET) -> onnx + aimet .encodings -> tflite
            (via qnn-onnx-converter).

        (3) (TORCHSCRIPT, TFLITE)

            (a) Fp32: Invalid option for model not subclass of AIMETQuantizableMixin

            (b) For AIMETQuantizableMixin subclass, torch(AIMET) ->
            torchscript with embedded quantizer -> tflite

        (4) (TORCHSCRIPT, QNN)

            (a) For fp32, torch -> qnn (via qnn-torch-converter, aka
                    --use_qnn_pytorch_converter flag in Hub)

            (b) For AIMETQuantizableMixin subclass, torch(AIMET) ->
            torchscript with embedded quantizer -> qnn (via
                    qnn-pytorch-converter)

    Returns:

    Path to source model that can be used directly with hub.upload_model or
    hub.submit_compile_job.
    """
    is_aimet = AIMETQuantizableMixin is not None and isinstance(
        model, AIMETQuantizableMixin
    )

    model_name = model.__class__.__name__

    compilation_options = model.get_hub_compile_options(target_runtime)

    if output_names is None:
        output_names = []

    if is_aimet:
        if source_model_format == SourceModelFormat.ONNX:

            def export_model_func():
                print("Exporting model to ONNX and generating AIMET encodings")
                return model.convert_to_onnx_and_aimet_encodings(
                    output_path,
                    model_name=model_name,
                    external_weights=external_onnx_weights,
                    output_names=output_names,
                )

        elif (
            source_model_format == SourceModelFormat.TORCHSCRIPT
            and target_runtime == TargetRuntime.TFLITE
        ):

            def export_model_func():
                print("Converting model to Torchscript")
                traced_model = model.convert_to_torchscript(
                    input_spec=input_spec, check_trace=check_trace
                )
                model_path = os.path.join(output_path, model_name + ".pt")
                os.makedirs(output_path, exist_ok=True)
                torch.jit.save(traced_model, model_path)
                return model_path

        else:  # Torchscript and QNN

            def export_model_func():
                print("Converting model to Torchscript and generating AIMET encodings")
                exported_model = model.convert_to_torchscript_and_aimet_encodings(  # type: ignore
                    output_path,
                    model_name=model_name,
                    input_spec=input_spec,
                )
                return exported_model

    else:  # fp32

        def export_model_func():
            traced_model = model.convert_to_torchscript(
                input_spec=input_spec, check_trace=check_trace
            )
            model_path = os.path.join(output_path, model_name + ".pt")
            os.makedirs(output_path, exist_ok=True)
            torch.jit.save(traced_model, model_path)
            return model_path

        if (
            target_runtime == TargetRuntime.TFLITE
            and source_model_format == SourceModelFormat.ONNX
        ):
            pass  # default is good

    if prepare_compile_options_only:
        return None, compilation_options
    else:
        return export_model_func(), compilation_options


def compile_zoo_model_to_hub(
    model: BaseModel,
    device: hub.Device,
    source_model_format: SourceModelFormat,
    target_runtime: TargetRuntime,
    calibration_data: DatasetEntries | None = None,
    input_spec: InputSpec | None = None,
    inference_options: str = "",
    check_trace: bool = True,
) -> HubModel:
    """
    Similar to `prepare_compile_zoo_model_to_hub`, but also performs the
    compilation on AI Hub and construct a HubModel object.
    """

    if input_spec is None:
        input_spec = model.get_input_spec()

    model_name = model.__class__.__name__

    with qaihm_temp_dir() as tmp_dir:
        assert tmp_dir is not None
        source_model, compilation_options = prepare_compile_zoo_model_to_hub(
            model=model,
            source_model_format=source_model_format,
            target_runtime=target_runtime,
            output_path=tmp_dir,
            check_trace=check_trace,
        )

        compile_job = hub.submit_compile_job(
            model=source_model,
            input_specs=input_spec,
            device=device,
            name=f"{model_name}_{source_model_format.name}_{target_runtime.name}",
            options=compilation_options,
            calibration_data=calibration_data,
        )
    assert isinstance(compile_job, hub.CompileJob)
    if not compile_job.wait().success:
        job_msg = compile_job.get_status().message or "(no job failure message)"
        raise ValueError(f"Compile job {compile_job} failed: {job_msg}")

    hub_model = compile_job.get_target_model()
    assert hub_model is not None
    input_names = list(model.get_input_spec().keys())
    return HubModel(
        hub_model,
        input_names,
        device,
        inference_options=inference_options,
    )


class HubModel(ExecutableModelProtocol):
    """
    Class that behaves like a pytorch model except when called, it runs an
        inference job on hub and returns a torch output.

    Intended to be passed as in input to app.py to run an app on-device.

    Parameters:
        input_names: List of input names to the model.
        device: Device on which to execute inference.
        hub_model_id: ID of Model stored in hub that will be used to run inference.
        model: If hub_model_id is absent, this model is compiled and used for inference.

    Returns:
        Callable that mimics the I/O of a torch model and evaluates inference on device.
    """

    def __init__(
        self,
        model: hub.Model,
        input_names: List[str],
        device: hub.Device,
        inference_options: str = "",
        output_names: Optional[List[str]] = None,
    ):
        self.model = model
        self.input_names = input_names
        self.device = device
        self.inference_options = inference_options
        self.output_names = [] if output_names is None else output_names

    def __call__(
        self,
        *args: torch.Tensor
        | np.ndarray
        | List[torch.Tensor | np.ndarray]
        | hub.Dataset
        | DatasetEntries,
    ) -> torch.Tensor | Tuple[torch.Tensor, ...]:
        return self.forward(*args)

    def forward(
        self,
        *args: torch.Tensor
        | np.ndarray
        | List[torch.Tensor | np.ndarray]
        | hub.Dataset
        | DatasetEntries,
    ) -> torch.Tensor | Tuple[torch.Tensor, ...]:
        target_runtime = (
            TargetRuntime.QNN if is_qnn_hub_model(self.model) else TargetRuntime.TFLITE
        )

        # Determine whether I/O is channel last
        channel_last_input, channel_last_output = "", ""
        if self.model.producer is not None:
            model_options = self.model.producer.options.strip().split()
            for option_num in range(len(model_options)):
                if model_options[option_num] == "--force_channel_last_input":
                    channel_last_input = model_options[option_num + 1]
                if model_options[option_num] == "--force_channel_last_output":
                    channel_last_output = model_options[option_num + 1]

        assert len(args) > 0, "At least 1 input should be provided for inference."

        dataset: hub.Dataset | DatasetEntries
        if isinstance(args[0], hub.Dataset) or isinstance(args[0], Mapping):
            # Use the existing provided dataset
            assert len(args) == 1, "Only 1 dataset can be provided for inference."
            dataset = args[0]
        else:
            # Create dataset from input tensors
            dataset = {}
            for name, inputs in zip(self.input_names, args):
                if not isinstance(inputs, (list, tuple)):
                    inputs = [inputs]  # type: ignore

                converted_inputs = []
                for input in inputs:
                    if isinstance(input, np.ndarray):
                        converted_inputs.append(input)
                    elif isinstance(input, torch.Tensor):
                        converted_inputs.append(input.detach().numpy())
                    else:
                        raise NotImplementedError(f"Unknown input type: {str(inputs)}")
                dataset[name] = converted_inputs

            # Transpose dataset I/O if necessary to fit with the on-device model format
            if channel_last_input:
                dataset = transpose_channel_first_to_last(
                    channel_last_input, dataset, target_runtime
                )

        inference_job = hub.submit_inference_job(
            model=self.model,
            inputs=dataset,
            device=self.device,
            name=f"{self.model.name}_demo_inference",
            options=self.inference_options,
        )
        assert isinstance(inference_job, hub.InferenceJob)
        if not inference_job.wait().success:
            job_msg = inference_job.get_status().message or "(no job failure message)"
            raise ValueError(f"Inference job {inference_job} failed: {job_msg}")

        output_ds_handle = inference_job.get_output_dataset()
        assert output_ds_handle is not None
        output_dataset = output_ds_handle.download()

        if channel_last_output:
            output_dataset = transpose_channel_last_to_first(
                channel_last_output,
                output_dataset,  # type: ignore
                target_runtime,
            )  # type: ignore

        outputs = output_dataset.values()  # type: ignore
        if len(self.output_names) > 0:
            outputs = [output_dataset[out_name] for out_name in self.output_names]  # type: ignore

        output_torch = [
            torch.from_numpy(np.concatenate(output, axis=0)) for output in outputs
        ]

        if len(output_torch) == 1:
            return output_torch[0]
        return tuple(output_torch)


def get_uploaded_precompiled_model(
    model_path: str,
    model_name: str,
    model_version: str,
    model_component: str,
    ignore_cached_model: bool = False,
):
    """
    Caches pre-compiled model in default asset path to be used in sub-sequence demos.
    """
    asset_config = ModelZooAssetConfig.from_cfg()
    model_id_path = asset_config.get_local_store_model_path(
        model_name, model_version, f"{model_component}_model_id.cached"
    )

    uploaded_model = None
    if not ignore_cached_model:
        try:
            with open(model_id_path, "r") as model_id_file:
                model_id = model_id_file.readline().strip()
            print(f"Using previously uploaded model({model_id}) for {model_component}")
            uploaded_model = hub.get_model(model_id=model_id)
            if uploaded_model is not None:
                return uploaded_model

        except Exception:
            pass

    # Upload model on hub
    uploaded_model = hub.upload_model(model_path)
    with open(model_id_path, "w") as model_id_file:
        model_id_file.writelines([f"{uploaded_model.model_id}"])
    return uploaded_model
