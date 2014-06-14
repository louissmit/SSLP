--
-- Created by IntelliJ IDEA.
-- User: louissmit
-- Date: 6/7/14
-- Time: 5:48 PM
-- To change this template use File | Settings | File Templates.
--

utils = {}

function utils.split(string)
    local res = {}
    for i in string.gmatch(string, "%S+") do
        table.insert(res, i)
    end
    return res
end

function utils.factorial(n)
        if n == 0 then
        return 1
      else
        return n * factorial(n-1)
      end
end



function utils.features(word_vecs, sent, left, right, flip, vector_size)
    if flip == nil then flip = false end
    if vector_size == nil then vector_size = 300 end

    local function get(i)
   		if i > 0 and i < #sent then
			return word_vecs:get(sent[i])
		else
			return torch.Tensor(vector_size)
        end
    end
    local sum = torch.Tensor(vector_size)
    for i = left+1, right-1 do
        sum:add(get(i))
    end
    if flip then
        left, right = right, left
    end
    local res = get(left-1)
    for _, i in pairs({left, left+1}) do
        res = torch.cat(res, get(i), 1)
    end
    res = torch.cat(res, sum, 1)
    for _, i in pairs({right-1, right, right+1}) do
        res = torch.cat(res, get(i), 1)
    end
    if res == nil then
        print(table.concat({unpack(sent, left, right)}, " "))
    end

    return res

end
return utils