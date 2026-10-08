# 09 — PC Bring-Up Checklist

**Do not install the full stack before inventorying the machine.**

The project targets ordinary personal hardware first.

Known planning assumption:

- ~16 GB system RAM;
- 5-6 CPU cores class;
- GPU exists but exact model/VRAM must be measured;
- desktop GPU may be upgraded;
- laptop may use Intel or hybrid graphics.

## Phase A — hardware inventory

Record for each machine:

```text
machine_name
Windows version
CPU exact model
physical cores
logical cores
RAM
GPU 1
GPU 1 VRAM
GPU 2 if present
driver version
CUDA available?
Vulkan available?
DirectML available?
free disk
Python version
Git version
```

## Windows quick checks

Possible commands:

```powershell
Get-CimInstance Win32_Processor |
  Select-Object Name,NumberOfCores,NumberOfLogicalProcessors

Get-CimInstance Win32_VideoController |
  Select-Object Name,AdapterRAM,DriverVersion

Get-CimInstance Win32_ComputerSystem |
  Select-Object TotalPhysicalMemory
```

If NVIDIA is present:

```text
nvidia-smi
```

Also record free disk space before downloading weights.

## Phase B — runtime decision

### NVIDIA GPU with enough VRAM

Prefer:

- CUDA path;
- stable-diffusion.cpp CUDA;
- PyTorch CUDA for perception experiments.

### Intel / AMD / low-VRAM

Evaluate:

- CPU inference;
- Vulkan;
- SYCL where supported;
- quantized GGUF/GGML paths;
- smaller perception/generation models.

### No useful local accelerator

Keep local:

- contracts;
- OS/MMonde integration;
- small models;
- replay;
- receipts;
- deterministic tests.

Use cloud/free endpoints only for heavy teacher/benchmark jobs.

## Phase C — install order

Do not install everything.

First PC bring-up target:

```text
1. project Python environment
2. one visual reader
3. one segmentation path
4. one depth path
5. EB-JEPA / transition lab
6. TD-MPC2 lab
7. stable-diffusion.cpp
8. one local generator
```

Only after measurement:

- ComfyUI;
- SANA;
- additional generators;
- WorldFM;
- video models.

## Phase D — baseline measurements

For every model:

```text
startup_time
peak_RAM
peak_VRAM
inference_latency
input_size
output_size
quality notes
failure mode
```

This data will determine routing.

Example future rule:

```text
if low_latency_required:
    use FAST_EYE
elif geometric_uncertainty_high:
    call depth adapter
elif local_generator_memory_too_high:
    use external teacher
```

Hardware limits become routing context, not a reason to redesign Obsidia.
