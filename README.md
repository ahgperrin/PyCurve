![Screenshot](logo.png)

-----------------
# PyCurve - Python Yield Curve Toolkit

-----------------
## What is it ? 

*PyCurve* is a Python package that provides to user high level 
yield curve usefull tool. For example you can istanciate a Curve 
and get a rate, a discount factor, even forward rate given multiple
methodology from Linear Interpolation to parametrization methods 
as Nelson Siegel or Bjork-Christenssen. PyCurve is also able to provide
solutions in order to build yield curve or price Interest rates derivatives 
via Vasicek or Hull and White.

-----------------

## Features 

Below this is the features that this package tackle :
- Curve Smoothing:
  - Create Curve Object with two numpy array (t,rt)
  - Linear interpolation given a Curve 
  - Cubic interpolation given a Curve 
  - Nelson Siegel and Svensson model creation and components plotting
  - Nelson Siegel and Svensson calibration given a Curve
  - Bjork Christensen and Augmented (6 factors) model creation and components plotting
- Stochastic Modelling:
  - Vasicek Model Simulation
  - Hull and WHite Model Simulation
  - Create Simulation Object given a simulation numpy array in order to get from 
    simulated model rate Curve, Discount Factor, Forward Rate...
  
- More to come:
  - CIR model will be implemented as soon as Euro Zone Rate will become positive.
  - Model Calibration
  - A "forward_curve" method will be implemented for each model in order to have directly 
    the whole forward curve x days in y days
    
-----------------

## How to install
From pypi
```sh
pip install PyCurve
```

From pypi specific version 
```sh
pip install PyCurve==0.0.2
```

From Git 
```sh
git clone https://github.com/ahgperrin/PyCurve.git
pip install -e . 
```

# Objects

## Curve Object

| Attributes  | Type    | Description                                 |
| :----------:|:--------| :-------------------------------------------|
| rt          | Private | Interest rates as float in a numpy.ndarray  |
| t           | Private | Time  as float or int in a numpy.ndarray    |

| Methods             | Type    | Description               | Return
| :------------------:|:--------| :-------------------------| :----------|
| get_rate            | Public  | rt getter                 | _rt        |
| get_time            | Public  | rt getter                 | _t         |
| set_rate            | Public  | rt getter                 | None       |
| set_time            | Public  | rt getter                 | None       |
| is_valid_attr(attr) | Private | Check attributes validity | attribute  |
| plot_curve()        | Public  | Plot Yield curve          | None       |

### Example

```sh
from PyCurve import Curve
rate = np.array([0.25, 0.5, 0.75, 1., 2., 
        3., 4., 5., 10., 15., 
        20.,25.,30.])
time = np.array([-0.63171, -0.650322, -0.664493, -0.674608, -0.681294,
        -0.647593, -0.587828, -0.51251, -0.101804,  0.182851,
        0.32962,0.392117,  0.412151])
curve = Curve(rate,time)
curve.plot_curve()
print(curve.get_rate)
print(curve.get_time)
```
```yaml

[-0.63171  -0.650322 -0.664493 -0.674608 -0.681294 -0.647593 -0.587828
 -0.51251  -0.101804  0.182851  0.32962   0.392117  0.412151]
  
[ 0.25  0.5   0.75  1.    2.    3.    4.    5.   10.   15.   20.   25.
 30.  ]

```
![Screenshot](example_screenshot/curve.png)

## Simulation Object 

| Attributes  | Type    | Description                                       |
| :----------:|:--------| :------------------------------------------------ |
| sim         | Private | Simulated paths matrix numpy.ndarray              |
| dt          | Private | delta_time  as float or int in a numpy.ndarray    |

| Methods                       | Type    | Description & Params                                                        | Return       |
| :--------------------------- :|:--------| :---------------------------------------------------------------------------| :------------|    
| get_sim                       | Public  | sim getter                                                                  | _rt          |
| get_nb_sim                    | Public  | nb_sim getter                                                               | sim.shape[0] |
| get_steps                     | Public  | steps getter                                                                | sim.shape[1] |
| get_dt                        | Public  | dt getter                                                                   | _dt          |
| is_valid_attr(attr)           | Private | Check attributes validity                                                   | attribute    |
| yield_curve()                 | Public  | Create a yield curve from simulated paths                                   | Curve        |
| discount_factor()             | Public  | Convert rate simulation to discount factor                                  | np.ndarray   |
| plot_discount_curve(average)  | Public  | Plot discount factor (average :bool False plot all paths True Plot estimate)| None         |
| plot_simulation()             | Public  | Plot Yield curve                                                            | None         |
| plot_yield_curve()            | Public  | Plot Yield curve                                                            | None         |
| plot_model()                  | Public  | Plot Yield curve                                                            | None         |
### Example
Using Vasicek to Simulate
```sh
from PyCurve.vasicek import Vasicek
vasicek_model = Vasicek(0.02, 0.04, 0.001, -0.004, 50, 30 / 365)
simulation = v.simulate_paths(20) #Return a Simulation and then we can apply Simulation Methods
simulation.plot_yield_curve()
```
![Screenshot](example_screenshot/simulated_curve.png)

```sh
simulation.plot_model()
```
![Screenshot](example_screenshot/simulation_example.png)