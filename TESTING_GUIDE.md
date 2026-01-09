# Testing Guide - Todo Full-Stack Application

## Overview
This guide provides step-by-step instructions to manually test all implemented features of the todo application.

**Prerequisites**:
- Backend running on http://localhost:8000
- Frontend running on http://localhost:3000
- Clean browser with no cached data (recommended)

---

## 1. Authentication Flow Testing

### 1.1 User Registration (/signup)

**Test Steps**:
1. Navigate to http://localhost:3000/signup
2. Observe page fade-in animation
3. Fill in registration form:
   - Email: `test@example.com`
   - Password: `SecurePassword123!`
   - Confirm Password: `SecurePassword123!`

**Expected Behavior**:
- ✅ Floating label animation on input focus
- ✅ Password strength indicator shows (weak → medium → strong)
- ✅ Color transitions: red → yellow → green
- ✅ Real-time validation feedback
- ✅ Success checkmark animation before redirect
- ✅ Automatic redirect to /dashboard after successful registration

**Error Cases to Test**:
- Email already exists → Error message with shake animation
- Password too weak → Validation error
- Passwords don't match → Validation error with shake animation
- Empty fields → Required field errors

### 1.2 User Login (/signin)

**Test Steps**:
1. Navigate to http://localhost:3000/signin
2. Fill in login form:
   - Email: `test@example.com`
   - Password: `SecurePassword123!`
3. Click "Sign In"

**Expected Behavior**:
- ✅ Floating label animations
- ✅ Loading state during API call
- ✅ Success animation before redirect
- ✅ JWT token stored in localStorage
- ✅ Redirect to /dashboard

**Error Cases to Test**:
- Wrong password → "Invalid credentials" error
- Non-existent email → "Invalid credentials" error
- Empty fields → Validation errors

### 1.3 Session Persistence

**Test Steps**:
1. After successful login, refresh the page
2. Manually navigate to /dashboard

**Expected Behavior**:
- ✅ User remains logged in (token persists)
- ✅ Dashboard loads without redirect to /signin

---

## 2. Task Management Testing (CRUD Operations)

### 2.1 Empty State

**Test Steps**:
1. Login with new user account
2. Navigate to /dashboard

**Expected Behavior**:
- ✅ Empty state component displays
- ✅ Animated illustration
- ✅ "Create your first task" message
- ✅ Call-to-action button

### 2.2 Create Task

**Test Steps**:
1. Click "Add Task" floating action button
2. Modal appears with slide-up animation
3. Fill in task details:
   - Title: `Complete project documentation`
   - Description: `Write comprehensive testing guide`
4. Click "Create"

**Expected Behavior**:
- ✅ Dialog opens with scale-in animation (desktop) or bottom-sheet (mobile)
- ✅ Form validation (title required)
- ✅ Loading state during API call
- ✅ Task appears in list immediately (optimistic UI)
- ✅ Modal closes automatically
- ✅ Success feedback

**Create Multiple Tasks**:
Create 5-10 tasks to test list animations:
- `Buy groceries`
- `Call dentist`
- `Review code changes`
- `Plan weekend trip`
- `Update resume`

**Expected Behavior**:
- ✅ Staggered list animation on initial load
- ✅ New tasks animate in smoothly
- ✅ Layout shift animation when tasks are added

### 2.3 Task Card Interactions

**Test Steps**:
1. Hover over a task card

**Expected Behavior**:
- ✅ Card lifts with shadow increase
- ✅ Edit and Delete buttons fade in on hover
- ✅ Smooth transition animations

### 2.4 Toggle Task Completion

**Test Steps**:
1. Click checkbox on a task card

**Expected Behavior**:
- ✅ Checkmark draw animation (SVG path animation)
- ✅ Strikethrough animation on title and description
- ✅ Opacity reduction (0.6)
- ✅ Immediate UI update (optimistic)
- ✅ Task marked as completed in database

**Test Unchecking**:
1. Click checkbox again on completed task

**Expected Behavior**:
- ✅ Checkmark disappears
- ✅ Strikethrough removed with reverse animation
- ✅ Full opacity restored

### 2.5 Edit Task

**Test Steps**:
1. Hover over task card
2. Click Edit button (pencil icon)
3. Modify title to: `Complete project documentation - Updated`
4. Click "Save"

**Expected Behavior**:
- ✅ Dialog opens with task details pre-filled
- ✅ Form validation works
- ✅ Task updates immediately in list
- ✅ Updated timestamp changes
- ✅ Smooth transition

### 2.6 Delete Task

**Test Steps**:
1. Hover over task card
2. Click Delete button (trash icon)
3. Confirm deletion (if confirmation dialog exists)

**Expected Behavior**:
- ✅ Task fades out
- ✅ Task slides left
- ✅ Remaining tasks reposition smoothly
- ✅ Task removed from database
- ✅ No console errors

### 2.7 Swipe-to-Delete (Mobile Only)

**Test Steps** (on mobile device or responsive mode):
1. Swipe task card to the left
2. Delete button appears
3. Complete swipe or tap delete

**Expected Behavior**:
- ✅ Drag gesture works smoothly
- ✅ Visual feedback during swipe
- ✅ Task deletes on complete swipe

---

## 3. Filtering & Search Testing

### 3.1 Filter Tabs

**Test Steps**:
1. Create mix of completed and active tasks (at least 3 of each)
2. Click "All" tab → See all tasks
3. Click "Active" tab → See only incomplete tasks
4. Click "Completed" tab → See only completed tasks

**Expected Behavior**:
- ✅ Animated sliding indicator follows active tab
- ✅ Task count badges update correctly
- ✅ Smooth fade-out/fade-in transitions
- ✅ Layout repositioning animation

### 3.2 Search Functionality

**Test Steps**:
1. Type in search box: `project`
2. Observe filtered results in real-time

**Expected Behavior**:
- ✅ Debounced search (300ms delay)
- ✅ Case-insensitive matching
- ✅ Searches both title and description
- ✅ Smooth fade transitions for filtered results
- ✅ Clear button appears when search has text

### 3.3 Sort Dropdown

**Test Steps**:
1. Click sort dropdown
2. Select different sort options:
   - Date (Newest First)
   - Date (Oldest First)
   - Title (A-Z)
   - Title (Z-A)

**Expected Behavior**:
- ✅ Dropdown menu fades in with slide-down animation
- ✅ Tasks reorder with smooth transitions
- ✅ Selected option highlighted
- ✅ Preserves current filter

### 3.4 Clear Filters

**Test Steps**:
1. Apply search and filter
2. Click "Clear filters" button

**Expected Behavior**:
- ✅ Button rotates on click
- ✅ All filters reset to default
- ✅ All tasks visible again

---

## 4. Responsive Design Testing

### 4.1 Mobile Layout (<640px)

**Test Steps**:
1. Resize browser to mobile width (375px)
2. Navigate through all pages

**Expected Behavior**:
- ✅ Single column layout
- ✅ Sidebar hidden
- ✅ Dialog becomes bottom sheet
- ✅ Touch targets minimum 44x44px
- ✅ All buttons easily tappable
- ✅ Text readable without zoom

### 4.2 Tablet Layout (640-1024px)

**Test Steps**:
1. Resize browser to tablet width (768px)

**Expected Behavior**:
- ✅ Two-column task grid
- ✅ Sidebar still hidden
- ✅ Navbar responsive
- ✅ Proper spacing

### 4.3 Desktop Layout (>1024px)

**Test Steps**:
1. Resize browser to desktop width (1440px)

**Expected Behavior**:
- ✅ Three-column task grid
- ✅ Sidebar visible with smooth width transition
- ✅ Centered modal dialogs
- ✅ All features accessible

---

## 5. Dark Mode Testing

### 5.1 Toggle Dark Mode

**Test Steps**:
1. Click theme toggle button in navbar
2. Observe color transitions

**Expected Behavior**:
- ✅ Sun/moon icon swap with rotation
- ✅ 300ms smooth transition on all colors
- ✅ Glassmorphism works in dark mode
- ✅ All text readable (WCAG AA contrast)
- ✅ Gradients appropriate for dark theme

### 5.2 Persistence

**Test Steps**:
1. Toggle to dark mode
2. Refresh page

**Expected Behavior**:
- ✅ Theme persists (localStorage)
- ✅ No flash of wrong theme

### 5.3 System Preference

**Test Steps**:
1. Clear localStorage
2. Set OS to dark mode
3. Open application

**Expected Behavior**:
- ✅ Detects system preference
- ✅ Applies dark mode automatically

---

## 6. Accessibility Testing

### 6.1 Keyboard Navigation

**Test Steps**:
1. Use only keyboard (Tab, Shift+Tab, Enter, Space, Escape)
2. Navigate through entire application

**Expected Behavior**:
- ✅ All interactive elements reachable
- ✅ Visible focus indicators (focus-ring)
- ✅ Logical tab order
- ✅ Escape closes modals
- ✅ Space toggles checkboxes
- ✅ Enter activates buttons

### 6.2 Focus Management

**Test Steps**:
1. Open task creation modal
2. Press Tab

**Expected Behavior**:
- ✅ Focus trapped in modal
- ✅ Can't tab outside modal
- ✅ Escape closes modal
- ✅ Focus returns to trigger button

### 6.3 ARIA Labels

**Test Steps**:
1. Inspect icon-only buttons
2. Check for aria-label attributes

**Expected Behavior**:
- ✅ All icon buttons have labels
- ✅ Screen readers can announce them
- ✅ Forms have proper labels

---

## 7. Animation & Performance Testing

### 7.1 Smooth Animations

**Test Steps**:
1. Open Chrome DevTools → Performance tab
2. Record while interacting with app
3. Check frame rate

**Expected Behavior**:
- ✅ 60fps during all animations
- ✅ No jank or stuttering
- ✅ GPU-accelerated (transform, opacity only)

### 7.2 Reduced Motion

**Test Steps**:
1. Enable "Reduce Motion" in OS settings
2. Reload application

**Expected Behavior**:
- ✅ Animations disabled or minimal
- ✅ Functionality still works
- ✅ No motion sickness triggers

### 7.3 Loading States

**Test Steps**:
1. Throttle network to "Slow 3G"
2. Perform operations

**Expected Behavior**:
- ✅ Loading skeletons display
- ✅ Spinner animations smooth
- ✅ No layout shift
- ✅ Error handling for timeouts

---

## 8. Error Handling Testing

### 8.1 Network Errors

**Test Steps**:
1. Disable network in DevTools
2. Try to create a task

**Expected Behavior**:
- ✅ Error message displays
- ✅ Retry button available
- ✅ Optimistic update rolls back
- ✅ No data loss

### 8.2 Validation Errors

**Test Steps**:
1. Try to submit empty task title
2. Try to use invalid email format

**Expected Behavior**:
- ✅ Inline error messages
- ✅ Shake animation on error
- ✅ Clear error messages
- ✅ Focus on error field

### 8.3 API Errors

**Test Steps**:
1. Stop backend server
2. Try operations

**Expected Behavior**:
- ✅ Graceful error handling
- ✅ User-friendly messages
- ✅ No crashes

---

## 9. Cross-Browser Testing

### 9.1 Browsers to Test
- ✅ Chrome (latest 2 versions)
- ✅ Firefox (latest 2 versions)
- ✅ Safari (latest 2 versions)
- ✅ Edge (latest 2 versions)

### 9.2 Mobile Browsers
- ✅ iOS Safari 14+
- ✅ Chrome Android 90+

### 9.3 Features to Verify
- ✅ Glassmorphism (backdrop-filter)
- ✅ CSS Grid layouts
- ✅ Framer Motion animations
- ✅ LocalStorage
- ✅ Fetch API

---

## 10. Edge Cases

### 10.1 Very Long Text

**Test Steps**:
1. Create task with 200+ character title
2. Create task with 1000+ character description

**Expected Behavior**:
- ✅ Text truncates with ellipsis
- ✅ Full text visible in edit modal
- ✅ No layout breaks

### 10.2 Rapid Clicks

**Test Steps**:
1. Click checkbox rapidly multiple times
2. Click create button multiple times

**Expected Behavior**:
- ✅ Debouncing prevents race conditions
- ✅ No duplicate tasks created
- ✅ Smooth animation completion

### 10.3 Large Task Lists

**Test Steps**:
1. Create 50+ tasks
2. Test scrolling and performance

**Expected Behavior**:
- ✅ Smooth scrolling
- ✅ No performance degradation
- ✅ All animations still work

### 10.4 Browser Zoom

**Test Steps**:
1. Test at 50% zoom
2. Test at 200% zoom

**Expected Behavior**:
- ✅ Layout adapts properly
- ✅ Text readable
- ✅ Buttons clickable
- ✅ Animations still work

---

## Testing Checklist Summary

Copy this checklist for quick testing:

### Authentication
- [ ] Registration with valid data
- [ ] Registration with duplicate email
- [ ] Login with valid credentials
- [ ] Login with invalid credentials
- [ ] Session persistence after refresh
- [ ] Logout functionality

### Task Management
- [ ] View empty state
- [ ] Create new task
- [ ] Edit existing task
- [ ] Toggle task completion
- [ ] Delete task
- [ ] Hover interactions on cards

### Filtering & Search
- [ ] Filter by All/Active/Completed
- [ ] Search by title/description
- [ ] Sort by date/title
- [ ] Clear all filters

### Responsive Design
- [ ] Mobile layout (<640px)
- [ ] Tablet layout (640-1024px)
- [ ] Desktop layout (>1024px)
- [ ] Swipe gestures on mobile

### Dark Mode
- [ ] Toggle dark mode
- [ ] Theme persistence
- [ ] System preference detection

### Accessibility
- [ ] Keyboard navigation
- [ ] Focus indicators visible
- [ ] ARIA labels present
- [ ] Screen reader compatible

### Performance
- [ ] 60fps animations
- [ ] Reduced motion support
- [ ] Loading states
- [ ] Error handling

### Cross-Browser
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge
- [ ] iOS Safari
- [ ] Chrome Android

---

## Automated Testing (Future Enhancement)

For future implementation, consider:
- **Unit Tests**: Component testing with Jest + React Testing Library
- **Integration Tests**: API endpoint testing with Pytest
- **E2E Tests**: Full user flow testing with Playwright
- **Visual Regression**: Screenshot comparison with Percy/Chromatic
- **Performance Tests**: Lighthouse CI for automated performance metrics

---

## Bug Reporting Template

If you find issues during testing, report using this format:

```markdown
**Bug**: [Short description]
**Severity**: Critical / High / Medium / Low
**Steps to Reproduce**:
1. Step 1
2. Step 2
3. Step 3

**Expected**: What should happen
**Actual**: What actually happens
**Browser**: Chrome 120.0.0
**Device**: Desktop / Mobile / Tablet
**Screenshot**: [Attach if applicable]
```

---

## Test Results Documentation

After completing tests, document results:

**Date**: [Test date]
**Tester**: [Your name]
**Browser**: [Browser and version]
**Device**: [Device type]

| Feature | Status | Notes |
|---------|--------|-------|
| Registration | ✅ Pass | All animations working |
| Login | ✅ Pass | - |
| Create Task | ✅ Pass | - |
| Edit Task | ✅ Pass | - |
| Delete Task | ✅ Pass | - |
| Filters | ✅ Pass | - |
| Search | ✅ Pass | - |
| Dark Mode | ✅ Pass | - |
| Responsive | ✅ Pass | - |
| Accessibility | ⚠️ Partial | Need screen reader testing |

---

**Note**: This is a comprehensive manual testing guide. For production deployment, automated testing should be implemented to ensure regression-free updates.
