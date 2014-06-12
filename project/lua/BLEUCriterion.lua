local BLEUCriterion, parent = torch.class('nn.BLEUCriterion', 'nn.Criterion')

function BLEUCriterion:__init()
   parent.__init(self)
   self.gradInput = torch.Tensor(1)
end

function BLEUCriterion:updateOutput(input,y)
   self.output=nil
   return self.output
end

function BLEUCriterion:updateGradInput(input, y)
    self.gradInput = nil
  return self.gradInput
end