--
-- Created by IntelliJ IDEA.
-- User: louissmit
-- Date: 6/7/14
-- Time: 2:14 PM
-- To change this template use File | Settings | File Templates.
--


function features(word_vecs, sent, left, right, flip)
    if flip == nil then flip = false end

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


function load_word_vecs(n)
    if n == nil then n = 1000 end
    local f = assert(io.open('../word_vecs_n='.. tostring(n) .. '.txt', "r"))
    local t = f:read()

    print(type(t))
    function split(string)
        local res = {}
        for i in string.gmatch(string, "%S+") do
            table.insert(res, i)
        end
        return res
    end
    shape = split(t)
    local word_vecs = torch.Tensor(tonumber(shape[1]), tonumber(shape[2]))
    local index = 1
    t = f:read()
    while t ~= nil do
        line = split(t)
        for i = 2, #line do
            word_vecs[index][i-1] = tonumber(line[i])
        end
        t = f:read()
    end
    f:close()
    return word_vecs
end

print(load_word_vecs()[1])