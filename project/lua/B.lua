features = require('utils').features

local B = {}

function B:new(mlp, word_vecs)
    self.mlp = mlp
    self.word_vecs = word_vecs
    self.matrix = {}
    self.__index = self
    return self
end

b_total = 0
b_right = 0
b_ratio_left = 0
b_ratio_right = 0

function B:get(sent, left_word, right_word)
--    local vector
--    if left_word > right_word then
--        vector = features(self.word_vecs, sent, right_word, left_word, true)
--    else
--        vector = features(self.word_vecs, sent, left_word, right_word)
--    end
--
--    local pred = self.mlp:forward(vector)[1]
--    if pred ~= pred then print(sent, left_word_right) end
--    local res
--    if pred > 0 then
--        res = 1
--    else
--        res = 0
--    end
--    if res == self.matrix[sent[left_word]][sent[right_word]] then
--        b_right = b_right + 1
--    else
--        if left_word > right_word then left_word, right_word = right_word, left_word end
--        b_ratio_left = b_ratio_left + (left_word / #sent)
--        b_ratio_right = b_ratio_right + (right_word / #sent)
--    end
--    b_total = b_total + 1

    --    return res
    --	return math.max(0, pred)

    return self.matrix[left_word][right_word]
end


function B:initHeuristically(gold)
    for i, left_word in pairs(gold) do
        if self.matrix[i] == nil then
            self.matrix[i] = {}
        end

        for j = i, #gold do
            if self.matrix[j] == nil then
                self.matrix[j] = {}
            end

            if self.matrix[i][j] == nil then
                self.matrix[i][j] = 1
            end

            if self.matrix[j][i] == nil then
                self.matrix[j][i] = 0
            end
        end
    end
end

return B
