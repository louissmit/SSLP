--
-- Created by IntelliJ IDEA.
-- User: louissmit
-- Date: 6/7/14
-- Time: 5:38 PM
-- To change this template use File | Settings | File Templates.
--
split = require('utils').split

local WordVecs = {}

function WordVecs:new(n)
    self.n = n
    self.word_vecs = nil
    self.mapping = {}
    self.__index = self
    return self
end

function WordVecs:get(word)
    local index = self.mapping[word]
    if index == nil then print(word) end
    return self.word_vecs[index]
end

function WordVecs:load_from_word2vec(filename)
    local f = assert(io.open(filename, "r"))
    local t = f:read()

    local shape = split(t)
    self.word_vecs = torch.Tensor(tonumber(shape[1]), tonumber(shape[2]))
    local index = 1
    local t = f:read()
    while t ~= nil do
        local line = split(t)
        local word = line[1]
        for i = 2, #line do
            self.word_vecs[index][i-1] = tonumber(line[i])
            self.mapping[word] = index
        end
        index = index + 1
        t = f:read()
    end
    f:close()
    return self
end

function WordVecs:save()
    torch.save('torch_wordvecs_n='..self.n, {self.word_vecs, self.mapping})
end

function WordVecs:load(n)
    self.n = n
    local res = torch.load('torch_wordvecs_n='..self.n)
    self.word_vecs = res[1]
    self.mapping = res[2]
end

return WordVecs