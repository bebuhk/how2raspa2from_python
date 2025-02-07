#! /bin/sh -f

# this script works similarly to to run_auto but takes the x, y and z 
# coordinate of the molecule from the script arguments $1, $2 and $3. 
export RASPA_DIR=${HOME}/RASPA/simulations/
export DYLD_LIBRARY_PATH=${RASPA_DIR}/lib
export LD_LIBRARY_PATH=${RASPA_DIR}/lib

# remove calculation folders
rm -rf RestartInitial                                                                                    
rm -rf CrashRestart
rm -rf Movies
rm -rf Output
rm -rf VTK
rm -rf Restart

# Check if exactly three arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <number1> <number2> <number3>"
    exit 1
fi

x=$1
y=$2
z=$3

# run initial simulation
awk '!found && /^RestartFile/ {print "#" $0; found=1; next} {print}' simulation.input > temp && mv temp simulation.input 
awk '!found && /^#CreateNumberOfMolecules/ {sub(/^#/, ""); found=1} {print}' simulation.input > temp && mv temp simulation.input    
$RASPA_DIR/bin/simulate $1 > /dev/null 2>&1

# copy restart file
cp -r Restart RestartInitial/

# delete (random) position of adsorbate created in initial simulation
sed -i '' '/^Adsorbate-atom/d' RestartInitial/System_0/*
# add desired adsorbate position to restart file
echo "Adsorbate-atom-position: 0 0    $x $y $z" >> RestartInitial/System_0/*
#echo "Adsorbate-atom-position: 0 0    -1.54928252, 17.45034191, 12.71675087" >> RestartInitial/System_0/*

# restart simulation
awk '!found && /^#RestartFile/ {sub(/^#/, ""); found=1} {print}' simulation.input > temp && mv temp simulation.input    
awk '!found && /^CreateNumberOfMolecules/ {print "#" $0; found=1; next} {print}' simulation.input > temp && mv temp simulation.input    
$RASPA_DIR/bin/simulate $1 > /dev/null 2>&1

# print energy results:
#grep -m1 -A4 "Host/Adsorbate energy:" Output/System_0/* #outputs the total energy (Host/Adsorbent), the LJ part, the Coulomb part, the 
#real part of the Coulomb and the fourier part of the Coulomb as text in seperate lines.
grep -m1 -A4 "Host/Adsorbate energy:" Output/System_0/* | awk '{print $NF}' # prints just the numerical values of the above mentioned energies

grep -m1 "Alpha convergence parameter" Output/System_0/* | awk '{print $NF}' # prints the alpha/kappa/smearing cooefficient RASPA used for the calculation
