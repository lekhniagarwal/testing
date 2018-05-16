#testing
import numpy as np
import pandas as pd
def load_experiment(experiments):
        
        if experiments.shape[0] > 0: #rows>0
            # if check_budget:
            if experiments['budget'].apply(lambda x: int(x) if pd.isnull(x)==False else 0).sum() > 0:
                    return experiments, 1
            else:
                if experiments['flow_probability'].sum() == 1:
                        return experiments, 0
        return pd.DataFrame(), 0


def map_user_experiment(kwargs,experiments):
        conditions = kwargs.get('conditions',{})
        experiments, budget_flag = load_experiment(experiments)
        if experiments.shape[0] > 0:
            #print(budget_flag)
            if budget_flag == 0:
                rnd = np.random.ranf()
                #print("vv")
                for index,row in experiments.sort_values(['flow_probability'],ascending = True).iterrows():
                    if rnd>row['flow_probability']:
                        return row['flow_id']
            elif budget_flag == 1:
                #print("vc")
                for index, row in experiments.iterrows():
                    #print(row['conditions'])
                    #print(conditions)
                    if conditions == row['conditions']:
                        return row['flow_id']
        return -1
		
		
		
def budget_utilization(user_experiment):
        budget_used = {'budget_used':[sum(user_experiment['budget_used'])]}
        budget_used = pd.DataFrame(data=budget_used)
        if budget_used.shape[0] == 0:
            return 0
        if budget_used['budget_used'][0] is None:
            return 0
        return budget_used['budget_used'][0]


		
		
def persist_user(kwargs,experiments,user_experiment):
        budget_assigned = kwargs.get('budget_used',0)
        flow_id = map_user_experiment(kwargs,experiments)
        #print(flow_id)
        experiments, budget_flag = load_experiment(experiments)
        if budget_flag == 1:
            budget = experiments['budget'].sum()
            budget_used = budget_utilization(user_experiment)
           # print(budget_used)
           # print(budget_assigned)
            #print(budget)
            if ((int(budget_used) + int(budget_assigned)) > budget):
                return -2
                #print("v")
        return flow_id
			
			
			

def get_user(kwargs,experiments,user_experiment,user_flow):
        
		
        
        if user_flow.shape[0] == 0: #using database by user_id
            return persist_user(kwargs,experiments,user_experiment)
        return user_flow['flow_id'][0]
    
	
def get_user_phone(kwargs,experiments,user_experiment,user_flow):
        
		
        
        if user_flow.shape[0] == 0: #use database by phone number then get users_id then use above fxn as it is
            return persist_user(kwargs,experiments,user_experiment)
        return user_flow['flow_id'][0]
    
	


	
import pytest
experiments1 = {'experiment_id': [1,2,3], 'flow_type': [3, 4,5],'flow_probability':[0.1,0.3,0.2],'budget':[100,None,129],'flow_id':[2,5,6],'conditions':['a','b','c']}
experiments1 = pd.DataFrame(data=experiments1)
	
experiments2 = {'experiment_id': [1,2,3], 'flow_type': [3, 4,5],'flow_probability':[0.1,0.7,0.2],'budget':[None,None,None],'flow_id':[2,5,6],'conditions':['a','b','c']}
experiments2 = pd.DataFrame(data=experiments2)
	
expected_output1 = (experiments1,1)
expected_output2 = (experiments2,0)
@pytest.mark.parametrize("test_input , expected_output",[(experiments1,expected_output1),(experiments2,expected_output2)])

#testing for load experiment function
def test_answer1(test_input, expected_output):
    result = load_experiment(test_input)
    assert  result == expected_output
	
	

#testing for map_user_experiment fxn
def test_answer2():
    experiments = {'experiment_id': [1,2,3], 'flow_type': [3, 4,5],'flow_probability':[0.1,0.3,0.2],'budget':[10,None,12],'flow_id':[2,5,6],'conditions':['a','b','c']}
    experiments = pd.DataFrame(data=experiments)
    kwargs = {"conditions" : 'a', "conditions1" : 'b', "conditions3" : "c","budget_used" : "20"}
    result = map_user_experiment(kwargs,experiments)
    assert  result == 2

#testing for budget_utilization fxn
def test_answer3():
    user_experiment = {'user_id': [1,2,3],'experiment_id': [1,2,3], 'budget_used': [3, 4,5], 'row status':['active','not_active','active'],'flow_id':[2,5,6]}
    user_experiment = pd.DataFrame(data=user_experiment)
    result = budget_utilization(user_experiment)
    assert  result == 12

#testing for persist_user fxn
def test_answer4():
    user_experiment = {'user_id': [1,2,3],'experiment_id': [1,2,3], 'budget_used': [3, 4,5], 'row status':['active','not_active','active'],'flow_id':[2,5,6]}
    user_experiment = pd.DataFrame(data=user_experiment)
    experiments = {'experiment_id': [1,2,3], 'flow_type': [3, 4,5],'flow_probability':[0.1,0.3,0.2],'budget':[10,None,12],'flow_id':[2,5,6],'conditions':['a','b','c']}
    experiments = pd.DataFrame(data=experiments)

    kwargs = {"conditions" : 'a', "conditions1" : 'b', "conditions3" : "c","budget_used" : "20"}


    result = persist_user(kwargs,experiments,user_experiment)
    assert  result == -2

#testing for get_user fxn
def test_answer5():
    user_experiment = {'user_id': [1,2,3],'experiment_id': [1,2,3], 'budget_used': [3, 4,5], 'row status':['active','not_active','active'],'flow_id':[2,5,6]}
    user_experiment = pd.DataFrame(data=user_experiment)
    experiments = {'experiment_id': [1,2,3], 'flow_type': [3, 4,5],'flow_probability':[0.1,0.3,0.2],'budget':[10,None,12],'flow_id':[2,5,6],'conditions':['a','b','c']}
    experiments = pd.DataFrame(data=experiments)
    kwargs = {"conditions" : 'a', "conditions1" : 'b', "conditions3" : "c","budget_used" : "20"}

    user_flow = {'user_id': [1,2,3],'experiment_id': [1,2,3],'flow_id':[2,5,6]}
    user_flow = pd.DataFrame(data=user_flow)
    result = get_user(kwargs,experiments,user_experiment,user_flow)
    assert  result == 2
	
	
#testing for get_user_phone fxn
def test_answer6():
    user_experiment = {'user_id': [1,2,3],'experiment_id': [1,2,3], 'budget_used': [3, 4,5], 'row status':['active','not_active','active'],'flow_id':[2,5,6]}
    user_experiment = pd.DataFrame(data=user_experiment)
    experiments = {'experiment_id': [1,2,3], 'flow_type': [3, 4,5],'flow_probability':[0.1,0.3,0.2],'budget':[10,None,12],'flow_id':[2,5,6],'conditions':['a','b','c']}
    experiments = pd.DataFrame(data=experiments)
    kwargs = {"conditions" : 'a', "conditions1" : 'b', "conditions3" : "c","budget_used" : "20"}

    user_flow = {'user_id': [1,2,3],'experiment_id': [1,2,3],'flow_id':[2,5,6]}
    user_flow = pd.DataFrame(data=user_flow)
    result = get_user_phone(kwargs,experiments,user_experiment,user_flow)
    assert  result == 2