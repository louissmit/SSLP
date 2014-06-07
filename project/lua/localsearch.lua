require "torch"
package.path = package.path .. "/?.lua"
B = require("B")
split = require('utils').split

function localSearch(B, sent)
	local n = table.getn(sent)
	local beta = torch.Tensor(n + 1, n + 1)
	local bp = torch.IntTensor(n + 1, n + 1)
	local delta = torch.Tensor(n + 1, n + 1, n + 1)

	for i = 1, n do
	 	beta[i][i+1] = 0
	 	for k = i+1, n+1 do
	 		delta[i][i][k] = 0
			delta[i][k][k] = 0
        end
    end

	for w = 2, n + 1 do
		for i = 1, n - w + 1 do
			local k = i + w
			beta[i][k] = -math.huge
			for j = i + 1, k-1 do
				delta[i][j][k] = delta[i][j][k - 1] + delta[i + 1][j][k] - delta[i + 1][j][k - 1] + B:get(sent, k - 1, i) - B:get(sent, i, k - 1)
				local new_beta = beta[i][j] + beta[j][k] + math.max(0, delta[i][j][k])

				if new_beta > beta[i][k] then
					beta[i][k] = new_beta
					bp[i][k] = j
                end
            end
        end
    end
    return delta, bp
end

local function traverseBackpointers(sent, delta, bp, i, k)

	if (k - i) > 1 then
        local j = bp[i][k]
        local left = traverseBackpointers(sent, delta, bp, i, j)
        local right = traverseBackpointers(sent, delta, bp, j, k)

        local res = {}
        if (delta[i][j][k] > 0) then
            left, right = right, left
        end
        for _, word in pairs(left) do
            table.insert(res, word)
        end
        for _, word in pairs(right) do
            table.insert(res, word)
        end
        return res

    else
		return {sent[i]}
  end

end

--input = {"b", "a", "d", "c"}
--sent_p = {"a", "b", "c", "d"}
b = B:new()
--b:initAlphabetically(input, sent_p)
--
--delta, bp = localSearch(B, input)
--
--print(table.concat(traverseBackpointers(input, delta, bp, 1, #input+1)))

function test_local_search(b)
    local f = assert(io.open('../../project2_data/training/p2_training.nl', "r"))

    local t = f:read()
    local x = 1
    while t ~= nil do
        local line = split(t)
        local sortedline = {unpack(line)}
        table.sort(sortedline)
        b:initHeuristically(line, sortedline)
        local delta, bp = localSearch(b, line)
--        print(sortedline)
        result = traverseBackpointers(line, delta, bp, 1, #line+1)
        print(x)
        x = x + 1
        t = f:read()
    end
    f:close()
end

test_local_search(b)
