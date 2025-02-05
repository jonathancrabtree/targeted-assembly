#!/usr/bin/env cwl-runner
cwlVersion: v1.0
label: Targeted Assembly -- run threaded alignment
class: CommandLineTool
stdout: alignment.out


requirements:
  - class: InlineJavascriptRequirement
  - class: EnvVarRequirement
    envDef:
      - envName: LD_LIBRARY_PATH
        envValue: $(inputs.python3_lib)


inputs:
  ea_map:
    label: Path to the output from extract_alleles.py
    type: File
    inputBinding:
      prefix: "--ea_map"

  assmb_map:
    label: Path to map from format_for_assembly.cwl
    type: File
    inputBinding:
      prefix: "--assmb_map"

  number_of_jobs:
    label: Number of alignment jobs to spawn
    type: int
    inputBinding:
      prefix: "--cpus"

  min_align_len:
    label: Minimum alignment length to perform alignment with (RATIO)
    type: double
    inputBinding:
      prefix: "--min_align_len"

  max_align_len:
    label: Maximum alignment length to perform alignment with (ABSOLUTE LENGTH)
    type: int?
    inputBinding:
      prefix: "--max_align_len"

  original_fsa:
    label: Path to where the unbuffered FASTA file generated from extract_sequences is
    type: File
    inputBinding:
      prefix: "--original_fsa"

  assmb_path:
    label: Path to the the directory to initialize directories for all the assembly output
    type: Directory
    inputBinding:
      prefix: "--assmb_path"

  assmb_type:
    label: Either "SPAdes" or "HGA". Determines how many assembled sequences are aligned to
    type: string
    inputBinding:
      prefix: "--assmb_type"

  priority:
    label: If given, the prefix of the sequence to solelys align to like XYZ.11203981.1 would require "XYZ" as input. Useful when trying to reconstruct a particular sequence
    type: string?
    inputBinding:
      prefix: "--priority"

  align_path:
    label: Path to output directory for all these alignments.
    type: Directory
    inputBinding:
      prefix: "--align_path"

  emboss_tool:
    label: Path to install directory of EMBOSS needle/water executable (e.g. /path/to/packages/emboss/bin/[needle|water])
    type: File
    inputBinding:
      prefix: "--emboss_tool"

  python3_lib:
    label: Path to allow Python3 to be found in the ENV
    type: string?


outputs:
  stdout:
    type: stdout


baseCommand: ["PYTHON3_EXE","TARGETED_ASSEMBLY_BIN/threaded_alignment.py"]