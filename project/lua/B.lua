
features = require('utils').features

local B = {}

function B:new(mlp, word_vecs)
    self.mlp = mlp
    self.word_vecs = word_vecs
  self.matrix = {}
  self.__index = self 
  return self
end

function B:get(sent, left_word, right_word)
--    local vector = features(self.word_vecs, sent, left_word, right_word)
--    local pred = self.mlp:forward(vector)[1]
--    if pred > 0 then
--        return 1
--    else
--        return 0
--    end
  return self.matrix[sent[left_word]][sent[right_word]]
end


function B:initHeuristically(gold)
		for i, left_word in pairs(gold) do
			if self.matrix[left_word] == nil then
				self.matrix[left_word] = {}
      end

			for j = i, #gold do
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
