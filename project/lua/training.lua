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

    local criterion = nn.ClassNLLCriterion()

    local function train_one_sample(input, output, learning_rate)
        criterion:forward(mlp:forward(input), output)

        -- train over this example in 3 steps
        -- (1) zero the accumulation of the gradients
        mlp:zeroGradParameters()
        -- (2) accumulate gradients
        mlp:backward(input, criterion:backward(mlp.output, output))
        -- (3) update parameters with a 0.01 learning rate
        mlp:updateParameters(learning_rate)
    end

    for g_prime in g_primes do
        for i = 1, #g_prime do
            for j = i+1, #g_prime do
                local true_vector = features(word_vecs, g_prime, i, j)
                train_one_sample(true_vector, 1, learning_rate)

                local false_vector = features(word_vecs, g_prime, i, j, true)
                train_one_sample(false_vector, 0, learning_rate)
            end
        end
    end
    return mlp
end


word_vecs = WordVecs:new()
word_vecs:load()
f = assert(io.open('../../project2_data/training/p2_training.nl', "r"))
t = f:read()
sent = split(t)
print(sent)
print(features(word_vecs, sent, 1, 5))
--train_nn()
--word_vecs:save()
--print(word_vecs)
--print(word_vecs:get('de'))
--features(word_vecs)
