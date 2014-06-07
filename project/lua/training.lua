--
-- Created by IntelliJ IDEA.
-- User: louissmit
-- Date: 6/7/14
-- Time: 2:14 PM
-- To change this template use File | Settings | File Templates.
--
WordVecs = require('word_vecs')

function features(word_vecs, sent, left, right, flip, vector_size)
    if flip == nil then flip = false end
    if vector_size == nil then vector_size = 300 end

    local function get(i)
   		if i >= 0 and i < #sent then
			return word_vecs[sent[i]]
		else
			return torch.Tensor(word_vecs.layer1_size)
        end
    end
    local sum = torch.Tensor(right - left)
    for i = left+1, right-1 do
        torch.add(sum, get(i))
    end
    if flip then
        left, right = right, left
    end
    local res = get(left-1)
    for i in {left, left+1} do
        res = torch.cat(res, get(i), 1)
    end
    res = torch.cat(res, sum, 1)
    for i in {right-1, right, right+1} do
        res = torch.cat(res, get(i), 1)
    end
    return res

end

word_vecs = WordVecs:new()
word_vecs:load()
--print(word_vecs)
print(word_vecs:get('de'))
--features(word_vecs)
