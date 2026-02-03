# PNL Tracker

The tracker has been hosted on my personal website. 

**Demo URL** : 
https://pnl-tracker.demo.ivorynoise.com/docs


## Flow
To test the flow manually using swagger: 
1. Please see the results using `/trades/` & `/portfolio` endpoint. I have added same test data to it as mentioned in pdf :)

The data can be seen here: https://pnl-tracker.demo.ivorynoise.com/api/v1/trades

1. Please clear all datastore before hitting any route.


## Design Choices

#### Choice 1: I implemented average-cost as the primary PnL method for simplicity and clarity
Logic is presented here
https://github.com/ivorynoise/pnl-tracker/blob/978053f5ac0eb6d9c478fbbca82439869ad73805/src/position/models.py#L51



### Choice 2: Use of Decimal class to avoid classical floating point errors that happen
I avoided any custom class/conversion as I wanted to focus on clarity and keep the excercise short. 

### Choice 3: Use of singleton classes
All datastores were mimiced using singleton classes

### Choice 4: Wrote tests for Positions 
Test coverage was considered only for positions as it is where the core logic lives

### Choice 5: No real time updates
The market price can be mimiced using `/api/v1/prices` endpoint. Also, I did not optimise for real-time pnl updates. The design and engineering decisions shown here will change for such features.

### Choice 6: Fee Avoidance
I did not consider fee while computing pnl


### Choice 7: Supports both long and short
In case the sellQty > buyQty, we allow shorting to showcase the pnl calculation. 


## Setup Guide
1. Build the program using `./build-run.sh`. This builds and pushes to registry. It can then be deployed via kubernetes.

2. To run locally, we can use the following command:
```
docker run -p 8000:8000 ivorynoise/pnl-tracker
```