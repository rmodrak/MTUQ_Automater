
To try out our automated MTUQ workflow, first install MTUQ_Automater 
following the instructions in INSTALL.txt

Then, simply invoke the scripts in order:

>> 1_download_waveforms.bash

>> 2_dowload_greens.bash

>> 3_generate_mtuq_scripts.bash

>> 4_run_mtuq_scripts.bash



Notes:

  - in step #1, observed waveforms will be downloaded for two seismic events

  - in step #2, Green's functions will be downloaded from a Green's function
    database hosted at github.com/rmodrak/greens_cps

  - the MTUQ script generator in step #3 works by substituting event-specific 
    origin time, location, and magnitude values into region-specific templates

  - the origin time, location and magnitude information values in step #3
    are preliminary/catalog values, which will be subsequently refined

  - if MPI is installed, feel free to invoke step #4 as

    >> 4_run_mtuq_scripts.bash <NPROC>

    where <NPROC> is the number of MPI processes over which to parallelize the
    main computational work

