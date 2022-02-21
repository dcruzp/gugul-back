class DocumentOutput:
  def __init__(self,betaL1 =0.1,betaG1 = 1.9):
    self.betaL1 = betaL1
    self.betaG1 = betaG1
    self.RR = []
    self.RI = []
    self.NR = []
    self.presition= []   
    self.recovery= []
    self.FL1= []
    self.FG1= []
    self.F1= [] 

  def CalculateStatistics(self):
    for i in range(len(self.RR)):
      RR = self.RR[i]
      RI = self.RI[i]
      NR = self.NR[i]

      rrUri = (len(RR | RI)) 
      rrUnr = (len(RR | NR))

      if rrUri !=0: presition = len(RR)/rrUri
      else: presition = 0

      if rrUnr !=0: recovery =  len(RR) /rrUnr
      else: recovery=0

      FL1 = ((1 + self.betaL1**2) * presition * recovery) / (self.betaL1*presition + recovery) if presition + recovery > 0 else 0
      FG1 = ((1 + self.betaG1**2) * presition * recovery) / (self.betaG1*presition + recovery) if presition + recovery > 0 else 0
      F1 = (2*presition * recovery) / (presition + recovery)  if presition + recovery > 0 else 0
      self.presition.append(presition)
      self.recovery.append(recovery)
      self.FL1.append(FL1)
      self.FG1.append(FG1)
      self.F1.append(F1) 



  def PrintAverages(self):
    print("\nCalculing Statistics...", end="")
    self.CalculateStatistics()
    print("\rDONE!!                      ")
    print("Averages: ")
    print('   Presicion:', self.mean(self.presition) )
    print('   Recobrado:', self.mean(self.recovery) )
    print('   F_(b<1):',self.mean( self.FL1) )
    print('   F_(b>1):', self.mean(self.FG1) )
    print('   F1:', self.mean(self.F1) )

  @staticmethod
  def mean( lis):
    return sum(lis) / len(lis)
 