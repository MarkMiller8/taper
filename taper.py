# Calculates optimal dosage tapering regimen for drugs with withdrawal effects (e.g. caffeine, nicotine, SSRIs, heroin, etc.) 
# Given a finite supply, assumes longest taper possible (as allowed by the supply) is most desirable
# Desired unknowns:  Duration of tapering regimen and required dosage for each day
# Parameters:  finalFraction (fraction of initial concentration remaining at end of regimen), tabletSupply, standardDosage

import math

halflife = 30. # hours
tabletSize = 20. # mg
tabletSupply = 26. # number of tablets at start of regimen
totalInitialSupply = tabletSize * tabletSupply # mg
currentSupply = totalInitialSupply
volume = 1. #  unit volume (one compartment, representing the body). 

deltaT = 1. # duration of timestep (hours)

standardDosage = 1*tabletSize # mg
currentDosage = standardDosage

initialConcentration = 0.
currentConcentration = initialConcentration
oldConcentration = initialConcentration
currentMinimumConcentration = initialConcentration
steadyStateConcentration = initialConcentration


hoursInDay = 24

steadyStateDuration = 20 * hoursInDay # change number of steadystate spinup days here
taperDuration = 52 * hoursInDay # change number of taper days here
totalDuration = steadyStateDuration + taperDuration

finalFraction = 0.1

file = open("taper.txt", "wb")

def writeToFile(file):

	file.write(str(timestep/24 - timestep%24 + 3))
	file.write(' ')
	file.write(str(currentConcentration))
	file.write(' ')
	file.write(str(currentDosage))
	file.write(' ')
	file.write(str(currentSupply))
	file.write("\n")

# Bring concentration to steady state


for timestep in range(0, totalDuration):


	if timestep % 24 == 0:

		if timestep <= steadyStateDuration:

			currentDosage = standardDosage

		if timestep > steadyStateDuration:
			
			idealConcentration = (finalFraction*steadyStateConcentration - steadyStateConcentration)/taperDuration*(timestep - steadyStateDuration) + steadyStateConcentration

			currentDosage = -1*standardDosage*(timestep - steadyStateDuration)/taperDuration + standardDosage
			currentSupply = currentSupply - currentDosage


		oldConcentration = currentConcentration					
		currentConcentration = oldConcentration + currentDosage - oldConcentration*math.log(2)*deltaT/halflife
		
		
		#writeToFile(file)
		

	else:
		oldConcentration = currentConcentration
		currentConcentration = oldConcentration - oldConcentration*math.log(2)*deltaT/halflife
		#writeToFile(file)
	

 	if timestep == steadyStateDuration - 1:
		steadyStateConcentration = currentConcentration

	if (timestep + 1) % 24 == 0:
		currentMinimumConcentration = currentConcentration

	if (timestep + 1) % 24 == 0 and timestep > steadyStateDuration:
		writeToFile(file)

		
file.close()




	

		 
