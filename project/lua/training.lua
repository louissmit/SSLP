--
-- Created by IntelliJ IDEA.
-- User: louissmit
-- Date: 6/7/14
-- Time: 2:14 PM
-- To change this template use File | Settings | File Templates.
--
WordVecs = require('word_vecs')
require('nn')
split = require('utils').split

function features(word_vecs, sent, left, right, flip, vector_size)
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
    return res

end

function train_nn(input_size, hu_size, g_primes, word_vecs)
    local mlp = nn.Sequential();  -- make a multi-layer perceptron
    local output_size = 1
    local learning_rate = 0.01

    mlp:add(nn.Linear(input_size, hu_size))
    mlp:add(nn.Tanh())
    mlp:add(nn.Linear(hu_size, output_size))

    local criterion = nn.MarginCriterion()

    local function train_one_sample(input, output, learning_rate)
        criterion:forward(mlp:forward(input), output)

        -- train over this example in 3 steps
        -- (1) zero the accumulation of the gradients
        mlp:zeroGradParameters()
        -- (2) accumulate gradients
        local mlp_out = mlp.output
--        print('mlpout', mlp_out)
        local error = criterion:backward(mlp_out, output)
--        print('error', error)
        mlp:backward(input, error)
        -- (3) update parameters with a 0.01 learning rate
        mlp:updateParameters(learning_rate)
    end

    local count = 1
    for _, g_prime in pairs(g_primes) do
        for i = 1, #g_prime do
            for j = i+1, #g_prime do
                local timer = torch.Timer()
                local true_vector = features(word_vecs, g_prime, i, j)
                train_one_sample(true_vector, 1, learning_rate)

                local false_vector = features(word_vecs, g_prime, i, j, true)
                train_one_sample(false_vector, -1, learning_rate)
                print(timer:time().real)
                print(count)
                count = count + 1
            end
        end
    end
    return mlp
end

function test_sample(word_vecs, g_primes, mlp)
   local total = 0
   local gut = 0
   for _, g_prime in pairs(g_primes) do
       print(g_prime)
        for i = 1, #g_prime do
            for j = i+1, #g_prime do
                local true_vector = features(word_vecs, g_prime, i, j)
                local res = mlp:forward(true_vector)
                if res[1] > 0 then
                    print(res[1])
                    gut = gut + 1
                end
                total = total + 1
                local false_vector = features(word_vecs, g_prime, i, j, true)
                local res = mlp:forward(false_vector)
                if res[1] < 0 then
                    print(res[1])
                    gut = gut + 1
                end
                total = total + 1
            end
        end
   end
   return gut, total
end

function main()
    local word_vecs = WordVecs:new()
    word_vecs:load(100000)
    local f = assert(io.open('../../project2_data/training/p2_training.nl', "r"))

    local train_set = {}
    local n = 0
    local train_size = 50
    local test_size = 10
    local sent_size = 10
    while n < train_size do
        local t = f:read()
        local sent = split(t)
        if #sent < sent_size then
            table.insert(train_set, sent)
            n = n + 1
        end
    end
    print(train_set)

    local mlp = train_nn(2100, 2400, train_set, word_vecs)
--    local test_set = {}
--    while (n - train_size) < test_size do
--        local t = f:read()
--        local sent = split(t)
--        if #sent < sent_size then
--            table.insert(test_set, sent)
--            n = n + 1
--        end
--    end

    local gut, total = test_sample(word_vecs, train_set, mlp)
    print(gut/total)
    return gut, total, mlp
end
gut, total, mlp = main()
--word_vecs = WordVecs:new()
--word_vecs:load_from_word2vec(100000)
--word_vecs:save()
