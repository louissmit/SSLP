
local B = {}

function B:new()
  self.matrix = {}
  self.__index = self 
  return self
end

function B:get(sent, left_word, right_word)
  return self.matrix[sent[left_word]][sent[right_word]]
end


function B:initHeuristically(sent, gold)
		for i, left_word in pairs(gold) do
			if self.matrix[left_word] == nil then
				self.matrix[left_word] = {}
      end
      
			for j = i, #sent do
				local right_word = gold[j]
				if self.matrix[right_word] == nil then
					self.matrix[right_word] = {}
        end
        
				if self.matrix[left_word][right_word] == nil then
					self.matrix[left_word][right_word] = 1
        end
        
				if self.matrix[right_word][left_word] == nil then
					self.matrix[right_word][left_word] = 0
        end
      end
    end
end
  
return B