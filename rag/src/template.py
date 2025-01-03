from liquid import Template

general_cot_system = '''You are a helpful medical expert, and your task is to answer a medical question. Please first think step-by-step and then give the answer for the provided options.Your responses will be used for research purposes only, so please have a definite answer.'''

general_cot = Template('''
Here is the question:
{{question}}

''')

general_medrag_system = '''You are a helpful medical expert, and your task is to answer a medical question using the relevant documents. First think step-by-step and then give the answer from the provided options.Your responses will be used for research purposes only, so have a definite answer.'''

general_medrag = Template('''
Here are the relevant documents:
{{context}}

Here is the question:
{{question}}


Please think step-by-step and generate your output:
''')



