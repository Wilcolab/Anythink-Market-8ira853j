/**
 * Express router for handling comments API.
 * @module routes/api/comments
 */

const router = require("express").Router();
const mongoose = require("mongoose");
const Comment = mongoose.model("Comment");

/**
 * Route for getting all comments.
 * @name GET /api/comments
 * @function
 * @async
 * @param {Object} req - Express request object.
 * @param {Object} res - Express response object.
 * @returns {Object} - JSON response containing all comments.
 */
router.get("/", async (req, res) => {
    try {
        const comments = await Comment.find();
        res.json(comments);
    } catch (err) {
        console.log(err);
    }
});

/**
 * Route for deleting a comment by ID.
 * @name DELETE /api/comments/:id
 * @function
 * @param {Object} req - Express request object.
 * @param {Object} res - Express response object.
 * @returns {Object} - JSON response indicating successful deletion.
 */
router.delete("/:id", (req, res) => {
    Comment.findByIdAndRemove(req.params.id)
        .then(() => {
        res.json({ });
        })
        .catch((err) => console.log(err));
    });

module.exports = router;
