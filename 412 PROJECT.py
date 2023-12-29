#Coding by Varak Mesropian

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns


#getting data from google form
data = pd.read_csv('ChatGPT - Response data - Form Responses 1.csv')

####################################################################################################################

#Figure 1.1
# Define a dictionary to map age ranges to numerical values
age_ranges = {'17-20': 0, '21-23': 1, '24-26': 2, '27-29': 3, '30-39': 4, '40-49': 5, '50+': 6}

#question
qAI = 'What AI tools are you familiar with / know about?'

# Split the 'AIs' column into separate columns for each AI (because in the form people were able to pick multiple answers)
data_AIs = data[qAI].str.get_dummies(', ')


# Merge the original DataFrame with the new 'AIs' DataFrame
data = pd.concat([data, data_AIs], axis=1)


#age question
qAge = 'What is your age?'

# Create a new column 'age_range' that maps the age ranges to numerical values
data['age_range'] = data[qAge].map(age_ranges)

# Group the DataFrame by age range and sum the values for each AI
AI_age_groups = data.groupby('age_range')[data_AIs.columns].sum()


# Plot each AI as a separate line in the line graph
fig, ax = plt.subplots()
for AI in AI_age_groups.columns:
    ax.plot(AI_age_groups[AI].index, AI_age_groups[AI].values, label=AI)


# Set the x-tick locations and labels
ax.set_xticks(list(age_ranges.values()))
ax.set_xticklabels(list(age_ranges.keys()))


# Set the number of ticks and labels for the y-axis
num_ticks = 20
max_count = AI_age_groups.values.max() #the max make it the greatest count
step = max_count / num_ticks #the number of each tick
tick_values = np.arange(0, max_count+step, step) #the values of each tick
tick_labels = ['{:,.0f}'.format(x) for x in tick_values] #the labels of the ticks

# Set the y-tick locations and labels
ax.set_yticks(tick_values)
ax.set_yticklabels(tick_labels)

# Add a legend and axis labels
ax.legend()
ax.set_xlabel('Age Range')
ax.set_ylabel('Count')
plt.title('Ages and which AI tools they have heard of', fontweight='bold')


####################################################################################################################

## FIGURE 1.2
#pie chart showing occupation

#question for occupation
qOcccup = 'What is your academic occupation?'

student = data.loc[data[qOcccup] == "Student (undergrad)"].count()[0] #getting number od undergrad students
prof = data.loc[data[qOcccup] == "Professor"].count()[0] #getting th number of professors
grad = data.loc[data[qOcccup] == "Graduate"].count()[0] #getting th number of graduates

labelOccup= ['Student (undergrad)', 'Professor', 'Graduate'] #the label

# calculate the percentage values
total = student + prof + grad #total number
student_pct = 100 * student / total #student percent
prof_pct = 100 * prof / total #prof percent
grad_pct = 100 * grad / total #graduate percent

# append the percentage values to the original labels
labelOccup_with_pct = [f'{l} ({p:.2f}%)' for l, p in zip(labelOccup, [student_pct, prof_pct, grad_pct])]


# plotting the chart
fig1, ax1 = plt.subplots()

fig1, ax1, autopct = ax1.pie(
    # the data of the pie chart
    [student, prof, grad],
    # setting colour
    colors=sns.color_palette('Set2'),
    # percentags, but I am not showing it
    autopct='',
    #so it starts at 90 degree angle
    startangle=90,
)

# update the legend labels
plt.legend(labelOccup_with_pct, title="answers: ", loc=(0.6, 0.1))

# Adding Title
occTitle ="What is your academic occupation?"
occTitle = plt.title(occTitle, fontsize=13, color='Black', fontweight='bold')
occTitle.set_position([0.5, 1.02])


####################################################################################################################

## FIGURE 1.3
#pie chart showing occupation

#question for occupation
qOcccup = 'What is your academic occupation?'

#question for field of study
qstudy = 'What is your field of study?'


# Filter the data to only include the occupation and field of study columns for only students
students_data = data[data[qOcccup] == 'Student (undergrad)'][[qstudy]]

# Create a frequency table of field of study of students
study_counts = students_data[qstudy].value_counts()


# Use the Seaborn Set2 palette
colors = sns.color_palette('Set2', n_colors=len(study_counts))


fig2, ax1 = plt.subplots()

# Create labels for each field of study and their frequency
labels = []
for study, count in study_counts.items():
    label = study + ': ' + str(count)
    labels.append(label)
    ax1.bar(study, count, color=colors[list(study_counts.index).index(study)]) #plotting the bars

# Add a legend showing the frequency of each field of study
plt.legend(labels, fontsize='small')

# Putting title and x, y labels
plt.title('Fields of Study for Undergraduate Students', fontweight = 'bold')
plt.xlabel('Field of Study')
plt.ylabel('Amount')


# Hide the x-axis labels
plt.xticks([])


####################################################################################################################

## FIGURE 1.4, FIGURE 1.5, FIGURE 1.6

#the types
CS = 'Computer Science'
LS = 'Life / Health Sciences'
BS = 'Business Studies'

def threeGraphs(type):
    # the questions
    qOcccup = 'What is your academic occupation?'
    qUsage = 'Since ChatGPT is very popular now days, what do you use this AI generator tool for?'
    qstudy = 'What is your field of study?'

    # Filter the data to only include the occupation and fruit columns for students
    students_data = data[(data[qOcccup] == 'Student (undergrad)') & (data[qstudy] == type)][qUsage]

    # Split the responses by comma
    split_responses = students_data.str.split(', ')

    # Create a new DataFrame to store the counts
    counts = pd.DataFrame(columns=['option', 'count'])

    # Loop through each split response and count the individual options
    for response in split_responses:
        for option in response:
            option_count = counts[counts['option'] == option]['count']
            if len(option_count) == 0:
                counts = pd.concat([counts, pd.DataFrame({'option': [option], 'count': [1]})], ignore_index=True)
            else:
                counts.loc[counts['option'] == option, 'count'] += 1


    # Use the Seaborn Set2 palette
    colors = sns.color_palette('Set2')


    fig3, ax1 = plt.subplots()
    # Create a bar plot
    for i, (option, color) in enumerate(zip(counts['option'], colors)):
        option_count = counts[counts['option'] == option]['count'].values[0]
        option_percent = option_count / len(students_data) * 100
        label = f"{option} ({option_percent:.1f}%)"
        ax1.bar(i, option_count, color=color, label=label)

    # Add a legend to the plot
    ax1.legend(fontsize='small')

    # Add axis labels and title
    plt.xlabel('Usage option')
    plt.ylabel('Count')
    plt.title('ChatGPT usage options for '+ type+ ' undergrad students',fontweight = 'bold', fontsize = 10)

    # Hide the x-axis labels
    plt.xticks([])

threeGraphs(CS) ## FIGURE 1.4
threeGraphs(LS) ## FIGURE 1.5
threeGraphs(BS) ## FIGURE 1.6



####################################################################################################################

##FIGURE 2.1

def oneToFive(question):
    # question about should GPT be allowed in Unis
    qUni = 'Do you think universities and schools should allow the use of ChatGPT?'

    # question abt dissabilities
    qFair = "Do you think that ChatGPT can be considered an unfair tool and can de a disadvantage to some students who do not have access to such AI generators?"

    #coloumn of the question
    column_to_graph = data[question]

    # Counting the number of responses for each option in the column
    response_counts = column_to_graph.value_counts()


    # Use the Seaborn Set2 palette
    colors = sns.color_palette('Set2')


    # Plot the data as a pie chart
    labels = response_counts.index
    sizes = response_counts.values

    fig4, ax1 = plt.subplots()
    ax1.pie(sizes, startangle=90, autopct='', colors = colors)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Add percentage to legend
    total = sum(sizes) #the totlal
    percentages = [(size/total)*100 for size in sizes] #the percent

    #making the label
    labels_legend = [f'{label} ({percentage:.1f}%)' for label, percentage in zip(labels, percentages)]
    #making the legend
    ax1.legend(labels_legend, loc="best")

    if(question == qUni):
        plt.title(question,fontsize = 10, fontweight = 'bold' )
    elif (question == qFair):
        # the tiltle of graph
        plt.title("ChatGPT unfair tool, for people that don't have (1 -> 5)", fontsize=8, fontweight='bold')

    else:
        # the tiltle of graph
        plt.title(question + ' (1 -> 5)', fontsize=8, fontweight='bold')



#question abt dissabilities
qDis = 'Do you think ChatGPT could help students with different learning disabilities?'

oneToFive(qDis) #calling function with the question

####################################################################################################################

##FIGURE 2.2
qCheat = "Do you think using ChatGPT is a form of cheating?"

oneToFive(qCheat) #calling function with the question



####################################################################################################################

##FIGURE 2.3

#question about reliability and bias
qRel = 'Do you think that ChatGPT can provide you with unbiased and reliable information?'

oneToFive(qRel) #calling function with the question


####################################################################################################################

##FIGURE 3.1
#question abt occupation
qOcccup = 'What is your academic occupation?'

#question about should it be harsh?
qHard = "Since AI generators do most of the work for you, do you think it's fair for professors to be harsher when grading your work?"


# Getting the professors answer for qHard
professor_data = data[data[qOcccup] == 'Professor'][[qHard]]

# Counting the number of "Yes" and "No" answers
yes_count = (professor_data == 'Yes').sum()[0]
no_count = (professor_data == 'No').sum()[0]


# Use the Seaborn Set2 palette
colors = sns.color_palette('Set2')


# Creating a pie chart
labels = ['Yes', 'No']
values = [yes_count, no_count]
fig11, ax1 = plt.subplots()
ax1.pie(values, autopct='', colors = colors)
ax1.set_title("Do professors think it's fair to be harsher when AI generators do the work?",fontsize = 10, fontweight = 'bold')

# Creating a list of strings with the labels and percentages
legend_labels = [f'{label}: {value/sum(values)*100:.1f}%' for label, value in zip(labels, values)]
# Putting legend
plt.legend(legend_labels)




####################################################################################################################

##FIGURE 3.2
#question about should GPT be allowed in Unis
qUni = 'Do you think universities and schools should allow the use of ChatGPT?'

oneToFive(qUni) #calling function with the question


####################################################################################################################
##PLOTTING ALL THE GRAPHS
plt.show()
