# OrientationLandscape

**OrientationLandscape** is a python package designed to analyze the relative orientation of two independently aligned domains of a biological complex in each particle image. By taking two .star files (each containing parameters from separate refinements of the same dataset) as inputs, the program computes how each particle’s first domain orientate relates to the second domain, generating a particle distribution “landscape” of orientation relationships. Users can then visualize, and select certain regions of this orientation landscape, and eventually map these selected particles back to the original .star file for further processing

## Table of Contents

*   [INSTALLATION](#installation)
*   [PREREQUISITES](#prerequisites)
*   [USAGE](#usage)
*   [EXAMPLE_WORKFLOW](#example_workflow)

## INSTALLATION:

1.  Clone the repository and cd inside

<!---->

    git clone https://github.com/yifancheng-ucsf/OrientationLandscape.git
    cd OrientationLandscape

2.  Create a conda environment with the required dependencies

<!---->

    conda env create -f environment.yml

3.  Activate the environment(always do this before using OrientationLandscape)

<!---->

    conda activate OrientationLandscape

## Prerequisites:

##### About the input: Two Star Files

The two .star files should have:

1, The same number of particles.

2, The same particle ordering (i.e., particle 1 in both .star files refers to the same image).

3, Each file should contain columns such as \_rlnAngleRot, \_rlnAngleTilt, \_rlnAnglePsi, \_rlnOriginXAngst, \_rlnOriginYAngst, etc.

##### Required Python Libraries

- numpy
- pandas
- matplotlib
- scipy
- mpi4py (for parallel execution)

##### MPI Environment (optional but recommended for parallel analysis)

If you want to run orientation\_analysis in parallel, you will need an MPI implementation like OpenMPI or MPICH.

## Usage:

Below is a brief usage summary for each of the four scripts. See the --help text for detailed arguments, default values, and optional flags.

#### orientation\_analysis

1, Computes the relative orientation of each particle by comparing the angles from two independent .star files.

2, Generates a CSV file containing per-particle orientation differences, translation differences, RND scores, etc.

3, The Related\_Neighbor\_Density(RND) is used to color and filter the points. It is a ratio representing local density around each data point, designed to remain comparable even if the number of particles changes across different datasets.

4, Can optionally compute and apply Inverse Mean Rotation (IMR) to align the orientation distribution.

*   Basic Usage (Serial):

<!---->

    orientation_analysi --s1 <star_file_1> --s2 <star_file_2> --o <output_prefix>

*   Parallel Usage(Recommended):

<!---->

    mpirun -n <X> orientation_analysis --s1 <star_file_1> --s2 <star_file_2> --o <output_prefix>

*   Arguments:

> \--s1 / --s2: The two input .star files to compute.

> \--o: Output prefix for the CSV files and other output.

> \--k: Number of nearest neighbors for RND calculation (default = 30).

> \--autoalign: If set, computes and applies IMR alignment, producing additional “\_after\_alignment.csv”.

> \--apply\_rotation: Apply a known rotation (ROT, TILT, PSI) to all particles before processing.

> \--outlier\_method: Method to identify outliers ('IQR' or 'Z-score').

#### landscape\_projection

1, Takes the CSV output from orientation_analysis and produces 2D projections of the orientation data (Euler angles, rotation vectors, etc.).

2, Plots histograms of rotation angles, distances, RND scores, etc.

3, Can generate Azimuth-Elevation maps if requested.

*   Usage:

<!---->

    landscape_projection --i <csv_file> --o <output_prefix>

*   Arguments:

> \--i: Input CSV file from orientation\_analysis.

> \--o: Output prefix for generated plots (.pdf/.png).

> \--bins: Number of bins in histograms (default = 50).

> \--vmin, --vmax: Color scale limits for scatter plots. Default would be the RND\_threshold and RND\_max.

> \--t: RND threshold to filter out low RND particles (fixed value)

> \--p: Percentage-based threshold (e.g., “keep top X% of RND”).
> - If neigher --t nor --p is set, the program defaults to use the value (RND\_max/3) to be the RND threshold.

> \--angle_limits: Limits for Euler angles: Euler01_min Euler01_max Euler02_min Euler02_max Euler03_min Euler03_max. default=[-180.0, 180.0, -180.0, 180.0, -180.0, 180.0]

> \--rotvec_limits: Limits for Rotation vectors: RotVec_X_min RotVec_X_max RotVec_Y_min RotVec_Y_max RotVec_Z_min RotVec_Z_max.',default=[-3.14, 3.14, -3.14, 3.14, -3.14, 3.14]
  

> \--generate\_azimuth\_elevation: If set, computes Azimuth/Elevation from rotation vectors and plots them.

#### point\_select

1, Filters a CSV file for particles whose Euler angles or rotation vectors fall within a certain spherical region (Alpha/Beta/Gamma space, or whichever space your columns represent).

2, Optionally further filters by additional labels/columns.

*   Usage:

<!---->

    point_select --i <csv_file> --c <Alpha> <Beta> <Gamma> --r <radius> [--o <output_csv>]

*   Arguments:

> \--i: Input CSV file (must have Alpha, Beta, Gamma columns).

> \--c: Center coordinates of the “sphere” in (Alpha, Beta, Gamma) space.

> \--r: Radius of the sphere.

> \--l: Optional label filtering

> \--o: Output CSV file with selected points. If not provided, it just prints how many points match without saving.

#### particle\_backtrack

1, Maps a subset of particles (specified by their ID column in the CSV file) back to the original .star file.

2, Produces a new .star file containing only the matching subset of rows.

*   Usage:

<!---->

      particle_backtrack --i <extracted_csv>  --s <original_star_file> --o <output_star_file>

*   Arguments:

> \--i: The CSV file containing selected particles. Must have an ID column.

> \--s: The original .star file with the full dataset.

> \--o: Name of the .star file to write the subset to.

## EXAMPLE_WORKFLOW:

##### Compute relative orientations relationship:

    mpirun -n 8 orientation_analysis --s1 domain1.star --s2 domain2.star --o domain1_against_domain2_orientation

This produces domain1\_against\_domain2.csv and domain1_against_domain2_orientation_outliers.csv(the points have been declude).
If --autoalign is used, also produces domain1\_against\_domain2\_after alignment.csv.

##### Visulize the orientation landscape:

    landcape_projection --i domain1_against_domain2.csv --o domain1_against_domain2_visualization --p 0.3 

This produces various .pdf and .png plots showing the projections in euler space or rotation vector space and histogram of RND and rotation angle and distance with the top 30% RND filtered points.

##### Select the points in a specified coordinate with a spherical region:

    point_select --i domain1_against_domain2.csv --c 13 0 14 --r 5  selected_points.csv

Here (13,0,14) in (Alpha, Beta, Gamma) space is the center and 5 is the radius, the selected points get saved to selected_points.csv.You can adjust the coordinate and radius as you need.

##### Backtrack the selected points to original star file:

    particle_backtrack --i selected_points.csv --s domain1.star  --o subset_domain1.star

Now you have a .star file containing only the subset of particles that fell within the spherical region in orientation space. You can use this subset for reconstruction, local refinement or further analysis.
