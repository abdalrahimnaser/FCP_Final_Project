----------------------------------
Opinion Dynamics Simulation  
----------------------------------

<h3>Overview:</h3>

This research uses a variety of models, such as the Defuant Model and the Ising Model, to mimic opinion dynamics within populations. It also has capability for simulating social networks to depict interpersonal relationships.</h1>

<h3>Packages required:</h3>

* matplotlib
* numpy
* argparse

<h3>Task 1 (Ising Model - Cole): </h3>

* Ising Model: This model represents agents as spins on a lattice and uses statistical mechanics to simulate opinion dynamics. Defuant Model: This model seeks to explain how people with different viewpoints interact with one another in order to determine if polarisation or consensus forms.  

* running: python FCP_assignment.py -ising_model (default model) followed by -external and -alpha for adjusting parameters.

* testing: python3 FCP_assignment.py -test_ising


<h3>Task 2 (Defuant Model - Abdalrahim):</h3>
  
* to run : use flag <em>-defuant</em> to run the model with defualt parameters of beta = 0.2, threshold = 0.2 .
* add flags <em>-beta</em> and <em>-threshold</em> after the previous command to configure the model parameters, where beta and threshold are floats from 0 to 1.
* use flag <em>-test_defuant</em> to run the automated model test.
* the population (number of opinions) of each iteration is fixed at 25.

<h3>Task 3 (Networks- Stephanos Prodromou):</h3> 

* To run/test: <em>-test network -network N </em> where N is an integer representing the size of the random network that will be created ( number of nodes it will have )  
* Fixed probability of connection of 0.5.  
* In order forr the results of the 3 functions to be printed, the plotted graph tab should be closed.  

<h3>Task 4 (Small World networks - Magoma Onkoba): </h3>

*  To get the visualization of ring network of a given size use the following code in the GitHub repository:
Python FCP_assignment.py -ring_network 20  
* To get the visualization of small world network with a re_wire probability very low, use the following code:
Python FCP_assignment.py -small_world 20 -re_wire 0.00001  
*  To get a small world network visualization with a default probability of 0.2 use the following code:
Python FCP_assignment.py -small_world 20  
* To get a small world network visualization with a probability very high use the following code:
Python FCP_assignment.py -small_world 20 -re_wire 0.98  
* These flags are case sensitive and they should be used as specified in the code examples.Probability should be between 0 and 1.





<h3>Task 5 (Modification to the defuant model to accept Network objects): </h3>

* the defuant model (task 2) was chosen here for modification to accept network objects  
* to run : use flags <em>-defuant </em> folowed by <em>-use_network N</em> where N is the number of nodes in the network  
* node connection probability is fixed at 0.5  



----------------------------------
Repo Link : https://github.com/abdalrahimnaser/FCP_Final_Project
----------------------------------
