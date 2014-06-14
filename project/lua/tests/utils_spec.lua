--
-- Created by IntelliJ IDEA.
-- User: louissmit
-- Date: 6/14/14
-- Time: 3:55 PM
-- To change this template use File | Settings | File Templates.
--
WordVecs = require('word_vecs')
require('torch')

describe("Features", function()
    local sent
    local vector
    local features
    local word_vecs

    setup(function()
        features = require("utils").features
        word_vecs = WordVecs:new()
        word_vecs:load(100000)
        sent = {"haben", "Sie", "das"}
        vector = features(word_vecs, sent, 0, 6, true)
    end)

    teardown(function()
    end)

--    before_each(function()
--        obj1 = { test = "yes" }
--        obj2 = { test = "yes" }
--    end)

    it("has correct size", function()
        assert.are.same(vector:size(1), 2100)
    end)

    it("sets up vars with the before_each", function()
        local isnan = false
        vector:apply(function(x)
            if x~=x then isnan = true end
        end)
        assert.is_not_true(isnan)
    end)
end)


