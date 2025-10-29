const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    // Get inputs from the action
    const token = core.getInput('github-token');
    const labelPrefix = core.getInput('label-prefix');
    
    // Create GitHub API client
    const octokit = github.getOctokit(token);
    
    // Get the pull request context
    const { context } = github;
    const { pull_request } = context.payload;
    
    if (!pull_request) {
      core.setFailed('This action can only be run on pull request events');
      return;
    }
    
    const { owner, repo } = context.repo;
    const pullNumber = pull_request.number;
    
    core.info(`Processing PR #${pullNumber} in ${owner}/${repo}`);
    
    // Get the list of changed files in the PR
    const { data: files } = await octokit.rest.pulls.listFiles({
      owner,
      repo,
      pull_number: pullNumber,
    });
    
    core.info(`Found ${files.length} changed files`);
    
    // Extract top-level directories from changed files
    const directories = new Set();
    
    files.forEach(file => {
      const path = file.filename;
      const topLevelDir = path.split('/')[0];
      
      // Only add as directory if it contains a slash (is actually a directory)
      if (path.includes('/')) {
        directories.add(topLevelDir);
      } else {
        // For files in root directory, use a special label
        directories.add('root');
      }
    });
    
    core.info(`Directories with changes: ${Array.from(directories).join(', ')}`);
    
    // Get existing labels on the PR
    const { data: existingLabels } = await octokit.rest.issues.listLabelsOnIssue({
      owner,
      repo,
      issue_number: pullNumber,
    });
    
    const existingLabelNames = new Set(existingLabels.map(label => label.name));
    
    // Create labels for each directory (if they don't exist)
    const labelsToAdd = [];
    
    for (const directory of directories) {
      const labelName = labelPrefix ? `${labelPrefix}${directory}` : directory;
      
      // Check if this label already exists on the PR
      if (existingLabelNames.has(labelName)) {
        core.info(`Label '${labelName}' already exists on PR`);
        continue;
      }
      
      // Try to create the label in the repository if it doesn't exist
      try {
        await octokit.rest.issues.getLabel({
          owner,
          repo,
          name: labelName,
        });
        core.info(`Label '${labelName}' already exists in repository`);
      } catch (error) {
        if (error.status === 404) {
          // Label doesn't exist, create it
          const labelColor = getLabelColor(directory);
          await octokit.rest.issues.createLabel({
            owner,
            repo,
            name: labelName,
            color: labelColor,
            description: `Changes in ${directory} directory`,
          });
          core.info(`Created new label '${labelName}' with color ${labelColor}`);
        } else {
          core.warning(`Error checking label '${labelName}': ${error.message}`);
        }
      }
      
      labelsToAdd.push(labelName);
    }
    
    // Add labels to the PR
    if (labelsToAdd.length > 0) {
      await octokit.rest.issues.addLabels({
        owner,
        repo,
        issue_number: pullNumber,
        labels: labelsToAdd,
      });
      core.info(`Added labels to PR: ${labelsToAdd.join(', ')}`);
    } else {
      core.info('No new labels to add');
    }
    
    // Set output
    core.setOutput('labels-added', labelsToAdd.join(','));
    core.setOutput('directories-changed', Array.from(directories).join(','));
    
  } catch (error) {
    core.setFailed(`Action failed with error: ${error.message}`);
  }
}

function getLabelColor(directory) {
  // Define colors for common directories
  const colorMap = {
    'src': '0052cc',      // Blue
    'test': '5319e7',     // Purple
    'tests': '5319e7',    // Purple
    'docs': '0e8a16',     // Green
    'doc': '0e8a16',      // Green
    'config': 'fbca04',   // Yellow
    'scripts': 'f9d0c4',  // Light orange
    'build': 'd93f0b',    // Red
    'ci': 'c2e0c6',       // Light green
    '.github': '1d76db',  // Dark blue
    'root': 'e4e669',     // Light yellow
  };
  
  return colorMap[directory] || 'ededed'; // Default gray color
}

// Run the action
run();