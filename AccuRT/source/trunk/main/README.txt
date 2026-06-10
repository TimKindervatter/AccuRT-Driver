To run AccuRT for the first time, the following environmental
variables have to be set (for bash shell) as follows:

export ACCURT_PATH=$HOME/path_to_the_AccuRT_directory
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ACCURT_PATH/lib
export PATH=$ACCURT_PATH/main:$PATH

On Mac OS X it should be DYLD_LIBRARY_PATH instead of LD_LIBRARY_PATH, e.g.:
export ACCURT_PATH=/Users/knut/AccuRT-binaries/AccuRT_v1.0.685
export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:$ACCURT_PATH/lib
export PATH=$ACCURT_PATH/main:$PATH

Once these variables are set in .bashrc, then open a new terminal window or run

  source ~/.bashrc

and then get information on how to run AccuRT like this

  AccuRT --help

or by running AccuRT without any arguments.
