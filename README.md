# NIRAL_DTI_PIPELINE

<h3> Pipeline flow diagram </h3>

![alt tag](https://github.com/munsellb/NIRAL_DTI_PIPELINE.git/pipeline_img.png)

<h3> Configuring and running the pipeline</h3>

There are two ways to run the pipeline: using the single-process version or using the multi-process version. To run the single process version from the command line type:

```python
python dti_pipeline.py –config config_pipeline.txt
```

and to run the the multi-process version form the command line type:

```python
python dti_pipeline_mp.py –config config_pipeline.txt
```

In general, the configuration file defines where the subject folder is located, a list that includes the subjects to be processed, the locations of the Autoseg computation and parameter files, and the pipeline components to be executed. For instance, on a Linux/UNIX/Mac operating system if the study folder is located at

```
/data/study_subjects
```

and in this folder the following sub-folders (typically named using subject specific unique ids) 

```
subject_id1
subject_id2
subject_id3
subject_id4
```
The subjects.txt file could be created using the command ```ls > subjects.txt```. Then the dti pipeline configuration file would have the following key-value pairs.

```
SubjectFolder:/data/study_subjects
SubjectList:/data/study_subjects/subjects.txt
```

For the autoseg template and pipeline component flag files, if the git rep was cloned in folder ```/data/git/NIRAL_DTI_PIPELINE``` then the dti pipeline configuration file would have the following key-value pairs.

```
COMPFILE:/data/git/NIRAL_DTI_PIPELINE/autoseg_templates/AutoSeg_Computation.txt
PARMFILE:/data/git/NIRAL_DTI_PIPELINE/autoseg_templates/AutoSeg_Parameters.txt
Flags:/data/git/NIRAL_DTI_PIPELINE/example_config/config_pipeline_flags.txt
```
In general, the flag file indicates the pipeline components to be executed. A ```yes``` value indicates the component will be executed, and a ```no``` value indicates the component will not be executed.

Example <a href="https://github.com/munsellb/NIRAL_DTI_PIPELINE.git/example_config">configuration files</a> and <a href="https://github.com/munsellb/NIRAL_DTI_PIPELINE.git/autoseg_templates">autoseg template</a> files can be found in the github repository. 


