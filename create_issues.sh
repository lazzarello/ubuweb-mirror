#!/bin/bash
# create_issues.sh - Convert TODO.md items to GitHub issues

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if gh is authenticated
if ! gh auth status > /dev/null 2>&1; then
    echo "Error: gh is not authenticated. Run 'gh auth login' first."
    exit 1
fi

echo -e "${BLUE}Creating GitHub issues for ubuweb-mirror TODO items...${NC}\n"

# High Priority Issues

echo -e "${GREEN}Creating High Priority issues...${NC}"

gh issue create \
  --title "Add FilmWork and SoundWork classes inheriting from Work" \
  --label "enhancement,high-priority" \
  --body "Extend the Work base class to support specialized handling for film and sound media types.

**Tasks:**
- [ ] Create FilmWork subclass inheriting from Work
- [ ] Create SoundWork subclass inheriting from Work
- [ ] Add type-specific validation and metadata handling
- [ ] Update tests

**Related files:** \`models.py\`"

gh issue create \
  --title "Write log parser for failed downloads" \
  --label "enhancement,high-priority,tooling" \
  --body "Build a tool to analyze download logs and identify failed downloads for retry/investigation.

**Tasks:**
- [ ] Parse log files to extract download failures
- [ ] Generate report of failed URLs
- [ ] Optionally support retry mechanism

**Related files:** New module, logging in \`models.py\`"

gh issue create \
  --title "Add SQLite ORM/Database layer" \
  --label "enhancement,high-priority,architecture" \
  --body "Include an ORM or database layer for tracking downloads, metadata, and state.

**Tasks:**
- [ ] Evaluate ORM options (SQLAlchemy, Peewee, etc.)
- [ ] Design schema for artists, works, downloads
- [ ] Implement database integration
- [ ] Add migration system

**Related files:** New module, refactor \`models.py\`"

# Medium Priority Issues

echo -e "${GREEN}Creating Medium Priority issues...${NC}"

gh issue create \
  --title "Improve artist identification system" \
  --label "enhancement,medium-priority" \
  --body "Build a better system to uniquely identify artists than array indexes based on DOM \`<a>\` tag order.

**Tasks:**
- [ ] Design stable artist ID system (URL-based? name-based?)
- [ ] Refactor code to use new IDs
- [ ] Handle edge cases (renamed artists, redirects)
- [ ] Update tests

**Related files:** \`models.py\`"

gh issue create \
  --title "Implement partial download detection and resume" \
  --label "enhancement,medium-priority" \
  --body "Implement detection and handling of partial/incomplete downloads.

**Tasks:**
- [ ] Check file size against Content-Length header
- [ ] Resume interrupted downloads
- [ ] Mark partial files for re-download
- [ ] Integration with file_index.py skip logic

**Related files:** \`models.py:81\`, \`file_index.py\`

**Note:** Currently \`file_index.py\` skips existing files but doesn't validate completeness.

See also: TODO_ANALYSIS.md"

gh issue create \
  --title "Extract description text from DOM" \
  --label "enhancement,medium-priority,parsing" \
  --body "Build conventions to extract untagged \"description\" text for artists and works.

**Tasks:**
- [ ] Identify description text patterns (siblings to \`<table>\` tags?)
- [ ] Implement extraction logic with word count threshold
- [ ] Handle edge cases and noise
- [ ] Store descriptions in metadata

**Related files:** \`models.py\`

**Challenge:** Description text is untagged and floating around the DOM. This will be tricky!"

gh issue create \
  --title "Build log analysis tool with statistics and graphs" \
  --label "enhancement,medium-priority,tooling" \
  --body "Write a tool to graph and analyze download statistics from logs.

**Tasks:**
- [ ] Parse logs for download metrics
- [ ] Generate statistics (speed, success rate, etc.)
- [ ] Create visualizations/graphs
- [ ] Export reports

**Related files:** New module"

# Low Priority Issues

echo -e "${GREEN}Creating Low Priority issues...${NC}"

gh issue create \
  --title "Refactor Page model with base class and URL-only interface" \
  --label "enhancement,low-priority,refactoring" \
  --body "Refactor Page class to only accept URL objects for all methods.

**Tasks:**
- [ ] Build URL class (see #URL_OBJECT_ISSUE)
- [ ] Update Page to accept URL objects only
- [ ] Remove artist object parameter handling
- [ ] Consider Page base class with subclasses for different page types

**Related files:** \`models.py:123\`

**Note:** This is an architectural improvement, not critical for functionality."

gh issue create \
  --title "Build URL object class" \
  --label "enhancement,low-priority,refactoring" \
  --body "Create a URL class to encapsulate URL handling and validation.

**Tasks:**
- [ ] Design URL class interface
- [ ] Migrate from string/urllib.parse usage
- [ ] Add validation and normalization
- [ ] Update all URL handling code

**Related files:** \`models.py:125\`

**Note:** Currently uses strings and urllib.parse. A URL class would provide better encapsulation."

gh issue create \
  --title "Extend broken links model for accurate state tracking" \
  --label "enhancement,low-priority" \
  --body "Extend broken links and zero-content pages model to always represent accurate broken state.

**Tasks:**
- [ ] Track broken links persistently
- [ ] Differentiate types of failures (404, timeout, zero bytes)
- [ ] Generate reports of broken content
- [ ] Historical tracking of link health

**Related files:** New module or extend \`models.py\`"

gh issue create \
  --title "Add email notification system for broken links" \
  --label "enhancement,low-priority,tooling" \
  --body "Add system to email site maintainers about broken links/issues.

**Tasks:**
- [ ] Collect broken link/content reports
- [ ] Format notification email
- [ ] Configure SMTP/email sending
- [ ] Schedule periodic reports

**Note:** Original TODO mentions \"Kenny G (NOT the WFMU person)\" - verify correct contact before implementing."

# Future Enhancements

echo -e "${GREEN}Creating Future Enhancement issues...${NC}"

gh issue create \
  --title "Optimize concurrent file existence checking" \
  --label "enhancement,performance,future" \
  --body "Optimize checking for existing downloads concurrently.

**Tasks:**
- [ ] Design concurrent file checking strategy
- [ ] Avoid race conditions
- [ ] Handle filesystem locking

**Related files:** \`models.py\`, \`file_index.py\`

**Note:** This will be challenging to implement correctly."

gh issue create \
  --title "Implement concurrent downloads" \
  --label "enhancement,performance,future" \
  --body "Implement parallel/concurrent downloading of multiple works.

**Tasks:**
- [ ] Design concurrent download architecture
- [ ] Add rate limiting
- [ ] Handle failures gracefully
- [ ] Configurable concurrency level"

gh issue create \
  --title "Experiment with alternative writing algorithms" \
  --label "enhancement,performance,future,research" \
  --body "Try different writing algorithms rather than linear order of \`<a>\` elements in DOM.

**Tasks:**
- [ ] Research optimal traversal strategies
- [ ] Implement alternative algorithms
- [ ] Benchmark and compare performance"

gh issue create \
  --title "Add command line arguments with click library" \
  --label "enhancement,future,ux" \
  --body "Add command line arguments using the \`click\` library.

**Tasks:**
- [ ] Define CLI interface
- [ ] Implement argument parsing with click
- [ ] Add help documentation
- [ ] Support common operations (download, analyze, report)"

gh issue create \
  --title "Develop reading chapter support" \
  --label "enhancement,future,feature" \
  --body "Extend support for the reading/text section of UbuWeb.

**Tasks:**
- [ ] Analyze reading section structure
- [ ] Implement reading-specific parsing
- [ ] Handle text/PDF downloads
- [ ] Add tests for reading content"

echo -e "\n${BLUE}All issues created successfully!${NC}"
echo -e "${YELLOW}View them at: https://github.com/lazzarello/ubuweb-mirror/issues${NC}"
