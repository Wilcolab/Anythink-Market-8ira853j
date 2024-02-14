/**
 * Express router for handling comment-related API routes.
 * @module routes/api/comments
 */

const router = require("express").Router();
const mongoose = require("mongoose");
const Comment = mongoose.model("Comment");

/**
 * GET /api/comments
 * Retrieves all comments.
 * @name GET/api/comments
 * @function
 * @async
 * @param {Object} req - Express request object.
 * @param {Object} res - Express response object.
 * @returns {Object} - JSON response containing the comments.
 */
router.get("/", async (req, res) => {
    try {
        const comments = await Comment.find();
        res.json({ comments });
    } catch (err) {
        console.log(err);
    }
});

/**
 * DELETE /api/comments/:id
 * Deletes a comment by its ID.
 * @name DELETE/api/comments/:id
 * @function
 * @param {Object} req - Express request object.
 * @param {Object} res - Express response object.
 * @returns {Object} - JSON response indicating success or failure.
 */
router.delete("/:id", (req, res) => {
    Comment.findByIdAndRemove(req.params.id)
        .then(() => {
            res.json({ success: true });
        })
        .catch((err) => console.log(err));
});

module.exports = router;
