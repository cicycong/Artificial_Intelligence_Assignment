#!/usr/bin/env python
# coding: utf-8

# # MBAN6500 Assignment1 
# ## Chang Cong

# ### Q1

# In[104]:


from experta import *


class Species(Fact):
    """
    require two percepts/declarations: cover and wings. 
    The former can take one of two val- ues, "fur" or "feathers", and the latter True or False.
    """
    cover = Field(str, mandatory=True)
    wings = Field(bool, mandatory=True)



class SpeciesIdentifier(KnowledgeEngine):    

    @Rule(
        Species(
            cover="feathers",
            wings=True))
    def speciesbird(self):
        print("The speices has fearthers and wings, so it is bird")

    @Rule(
        Species(
            cover="fur",
            wings=True))
    def speciesmammal(self):
        print("The speices has fur and wings, so it is mammal")
        
    @Rule(
        Species(
            cover="feathers",
            wings=False))
    def speciesunknown(self):
        print("The speices have feathers but doesn't have wings, so it is unknown")


speicesengine = SpeciesIdentifier()
speicesengine.reset()



# add declarations here to tells whether an animal is a bird, mammal, or unknown
speicesengine.declare(Species(cover="feathers",wings=True))
#speicesengine.declare(Species(cover="fur",wings=True))
#speicesengine.declare(Species(cover="feathers",wings=False))
speicesengine.run()


# ### Q2



class Multispecies(Fact):
    """
    require five percepts/declarations: single, backbones, breath, cover, wings.
    
    If single is false, meaning that it is single-cell animial, whichi is protozoa.
    If single is true and backbones is false, then it is an invertebrate.
    If single is false and backbones is false, then it is vertebrates, which includes fish, bird, mammal and unknown.
    
    For a vertebrates,
    If it breath in gills then it is a fish, otherwise it is a bird, mammal or unknown.
    When the speices breath in lungs, if it has feathers cover and the wings is true, it is a bird.
    If it has fur cover and has wings, it is a mammal.
    If it has feathers and no wings, it is unknown.
    
    """
    single= Field(bool, mandatory=True) 
    backbones= Field(bool, mandatory=False) 
    breath= Field(str, mandatory=False) #gills/lungs 
    cover = Field(str, mandatory=False) #fur/feather 
    wings = Field(bool, mandatory=False)



class AnimalIdentifier(KnowledgeEngine):    

    @DefFacts()
    def animals(self):
        yield Multispecies(single=False,backbones=True,breath="lungs",cover="feather",wings=True)
 
        
    #define protozoa
    @Rule(
        Multispecies(
            single=True))
    def protozoa(self):
        print("It is protozoa.")

    #define invertebrate
    @Rule(
        Multispecies(
            single=False,
            backbones=False))
    def invertebrate(self):
        print("It is invertebrate.")

    #define invertebrate
    @Rule(
        Multispecies(
            single=False,
            backbones=True,
            breath="gills"))
    def fish(self):
        print("It is fish.")
    
    #define bird
    @Rule(
        Multispecies(
            single=False,
            backbones=True,
            breath="lungs",
            cover="feathers",
            wings=True))
    def bird(self):
        print("It is bird.")
    
    #define mammal
    @Rule(
        Multispecies(
            single=False,
            backbones=True,
            breath="lungs",
            cover="fur",
            wings=True))
    def mammal(self):
        print("It is mammal.")
    
    #define unknown
    @Rule(
        Multispecies(
            single=False,
            backbones=True,
            breath="lungs",
            cover="feathers",
            wings=False))
    def mammal(self):
        print("It is unknown.")
        


animalengine = AnimalIdentifier()
animalengine.reset()

# add declarations
animalengine.declare(Multispecies(single=False,
            backbones=True,
            breath="lungs",
            cover="feathers",
            wings=False))
animalengine.run()


#declaration "single" is mandatory field for the Fact, you must include it in the engine to proceed.
animalengine.declare(Multispecies(single=True))
animalengine.run()


animalengine.declare(Multispecies(single=False,backbones=False))
animalengine.run()


# ### Q3

# I designed an expert system that helps people determine whether to accept or decline an offer after receiving it. 

# The system measures in three dimensions: **Salary, Location and Culture of the Company**.  The users only need to type **yes** or **no** as an answer.Any of them that doesn't meet the expectation would lead to the decline of the offer. When all of these three critiras are met, it will suggest accept the offer.

# The system asks **3** questions in total.
# 
# The first question is about the salary. It will ask "*Does the salary higher than $5000/month?*". 
# If the answer is no it will suggest decline the offer. If the answer is yes, it will come to the location question:"*Is the office near home?*". If the location criteria is also met, the last question that inquires the culture will show up:"*Does the culture of company fit your value?*" If the answers to the three question are yes, it will print "*Congratulations. Accepted the offer.*".


class joboffer(KnowledgeEngine):
    @DefFacts()
    def _received_offer(self):
        yield Fact(job="offered")

    # Rule 1:Is the salary satisfactory
    @Rule(Fact(job='offered'), NOT(Fact(salary=W())))
    def ask_salary(self):
        self.declare(
            Fact(salary=input("Does the salary higher than $5000/month? (yes/no)")))
        
    # Rule 2:Is the location satisfactory
    @Rule(Fact(job='offered'), (Fact(salary='yes')))
    def ask_location(self):
        self.declare(
            Fact(location=input("Is the office near home? (yes/no)")))
        
    # Rule 3:Does the culture fit your value
    @Rule(Fact(job='offered'), (Fact(salary='yes')), (Fact(location='yes')))
    def ask_culture(self):
        self.declare(
            Fact(culture=input("Does the culture of company fit your value? (yes/no) ")))
    
    # Decline because of salary
    @Rule(Fact(job='offered'), (Fact(salary='no')))
    def decline1(self):
        print("The salary is lower than expected. Decline the offer.")
    
    # Decline because of location
    @Rule(Fact(job='offered'), (Fact(salary='yes')),(Fact(location='no')))
    def decline2(self):
        print("The offcie is too far away from home. Decline the offer.")
    
    # Decline because of location
    @Rule(Fact(job='offered'), (Fact(salary='yes')),(Fact(location='yes')),(Fact(culture='no')))
    def decline3(self):
        print("The culture doesn't fit my value. Decline the offer.")
    
    # accept the offer
    @Rule(Fact(job='offered'), (Fact(salary='yes')),(Fact(location='yes')),(Fact(culture='yes')))
    def accept(self):
        print("Congratulations. Accepted the offer.")




offerengine = joboffer()
offerengine.reset()
offerengine.run()






