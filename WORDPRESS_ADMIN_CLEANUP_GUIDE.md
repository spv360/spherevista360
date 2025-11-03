# WordPress Admin - Duplicate Pages Cleanup Guide

**Last Updated:** November 2, 2025  
**Estimated Time:** 20-30 minutes  
**Risk Level:** Low (pages go to Trash, not permanently deleted immediately)

---

## 🎯 **Objective**

Remove all duplicate calculator pages from WordPress admin and keep only the most recent, functional versions.

---

## 📋 **Pre-Cleanup Checklist**

Before starting, ensure:

- [ ] You have WordPress admin access
- [ ] You've backed up the site (or can export pages)
- [ ] You understand which pages to keep (see list below)
- [ ] You have 20-30 minutes to complete this task
- [ ] No one else is editing pages simultaneously

---

## 🚀 **Step-by-Step Process**

### **Step 1: Backup Your Pages**

1. Login to WordPress Admin: https://spherevista360.com/wp-admin/
2. Go to **Tools** → **Export**
3. Select **Pages**
4. Click **Download Export File**
5. Save the file as `spherevista360-pages-backup-2025-11-02.xml`

✅ **Checkpoint:** You now have a backup of all pages

---

### **Step 2: Access Pages List**

1. In WordPress Admin, go to **Pages** → **All Pages**
2. You should see a list of all pages
3. At the top right, click **Screen Options**
4. Set "Number of items per page" to **100** (to see more at once)
5. Click **Apply**

✅ **Checkpoint:** You can now see most/all pages on one screen

---

### **Step 3: Identify Duplicate Calculator Pages**

Look for pages with calculator-related names. Common duplicates to check:

#### **Known Duplicate Sets:**

**Retirement Planner:**
- Look for "Retirement Planner and Estimator" or "Retirement Planner"
- Check for multiple pages with same title
- **Keep:** Page ID **3173** (or newest version)
- **Delete:** Page ID **3217** (or older versions)

**Tax Calculators:**
- "Federal Income Tax Calculator"
- "State Income Tax Calculator"
- "Capital Gains Tax Calculator"
- "Self-Employment Tax Calculator"
- "Retirement Tax Calculator"
- "Tax Withholding Calculator"

**Investment Calculators:**
- "Lump Sum Investment Calculator"
- "SIP Calculator"
- "Compound Interest Calculator"

**Other Calculators:**
- "Loan EMI Calculator"
- "US Tax Calculator Suite" (landing page)

**How to Spot Duplicates:**
- Pages with numbers in URL slug (e.g., `calculator-2`, `calculator-3`)
- Pages with "copy", "old", "test", "backup" in title
- Multiple pages with same title but different modified dates
- Pages created on same date with similar titles

---

### **Step 4: Sort to Find Duplicates**

#### **Method A: Sort by Title**
1. Click the **"Title"** column header to sort alphabetically
2. Duplicate pages will appear next to each other
3. Compare their "Modified" dates
4. Keep the most recently modified one

#### **Method B: Sort by Date**
1. Click the **"Date"** column header to sort by date (newest first)
2. Look for pages created on same day with similar titles
3. These are likely deployment duplicates

#### **Method C: Search by Keyword**
1. Use the search box to search for specific terms:
   - "calculator"
   - "retirement"
   - "tax"
   - "investment"
2. Review all results for duplicates

---

### **Step 5: Identify Which Page to Keep**

For each duplicate set, **KEEP the page that:**
- ✅ Has the most recent "Modified" date
- ✅ Has the correct URL slug (without numbers like "-2", "-3")
- ✅ Has working functionality when you preview it
- ✅ Has the most content/features

**DELETE pages that:**
- ❌ Have older "Modified" dates
- ❌ Have numbered slugs (e.g., `retirement-planner-estimator-2`)
- ❌ Have "test", "old", "copy", "backup" in title
- ❌ Don't work properly when previewed

---

### **Step 6: Delete Duplicate Pages**

For each duplicate page you want to DELETE:

1. **Hover** over the page title
2. Click **"Trash"** (appears below title on hover)
3. Confirm by clicking **"Move to Trash"** if prompted

**DO NOT click "Delete Permanently" yet!**

Pages in Trash can be restored for 30 days.

---

### **Step 7: Verify Pages in Trash**

1. Click **"Trash"** link at the top of the Pages list
2. Review all trashed pages
3. Make sure you didn't accidentally trash important pages
4. If you see a page that shouldn't be deleted:
   - Hover over it
   - Click **"Restore"**

---

### **Step 8: Update Retirement Planner (CRITICAL)**

The retirement planner needs special attention as it just got major fixes:

1. Find **"Retirement Planner and Estimator"** page (should be ID 3173)
2. Click **"Edit"**
3. At the top right, look for three dots menu (⋮) or "Code editor" toggle
4. Switch to **"Code editor"** mode (or "Text" tab if you see it)
5. **Select ALL content** in the editor (Ctrl+A or Cmd+A)
6. **Delete** all content
7. Open the file `/home/kddevops/projects/spherevista360/retirement-planner-fixed.html` on your computer
8. Copy everything BETWEEN (not including) the `<body>` and `</body>` tags
9. **Paste** into WordPress editor
10. Click **"Update"** button (top right)
11. Click **"Preview"** to verify it looks correct

✅ **Checkpoint:** Retirement planner should now have:
- Aligned labels with icons
- Horizontal button layout
- Interactive data displays
- Progress bars and charts
- No JavaScript errors

---

### **Step 9: Verify Other Key Calculators**

Test each calculator to ensure it works:

1. Go to **Pages** → **All Pages**
2. For each calculator page:
   - Click page title to view on frontend
   - Verify the calculator loads
   - Try entering test values
   - Click calculate button
   - Verify results appear correctly
   - Check mobile view (responsive)

**Test These Pages:**
- [ ] Federal Income Tax Calculator
- [ ] State Income Tax Calculator
- [ ] Capital Gains Tax Calculator
- [ ] Self-Employment Tax Calculator
- [ ] Retirement Tax Calculator
- [ ] Tax Withholding Calculator
- [ ] Lump Sum Investment Calculator
- [ ] Retirement Planner and Estimator ⭐ (most important)
- [ ] SIP Calculator
- [ ] Compound Interest Calculator
- [ ] Loan EMI Calculator

---

### **Step 10: Permanently Delete (Optional)**

**WAIT AT LEAST 24-48 HOURS** before doing this step!

After verifying everything works:

1. Go to **Pages** → **Trash**
2. Review all trashed pages one more time
3. Click **"Empty Trash"** button
4. Confirm deletion

⚠️ **WARNING:** This permanently deletes pages. They cannot be recovered!

---

### **Step 11: Clear All Caches**

After cleanup, clear caches to ensure visitors see updated pages:

#### **WordPress Cache Plugins:**

**If using WP-Optimize:**
1. Go to **WP-Optimize** → **Cache**
2. Click **"Purge cache"** or **"Delete all cache files"**

**If using LiteSpeed Cache:**
1. Go to **LiteSpeed Cache** → **Purge**
2. Click **"Purge All"**

**If using W3 Total Cache:**
1. Go to **Performance** → **Dashboard**
2. Click **"Empty All Caches"**

**If using WP Super Cache:**
1. Go to **Settings** → **WP Super Cache**
2. Click **"Delete Cache"**

#### **Server Cache:**
Run this command if you have SSH access:
```bash
bash /home/kddevops/projects/spherevista360/clear_cache.sh
```

#### **Browser Cache:**
- Press **Ctrl+Shift+R** (Windows/Linux) or **Cmd+Shift+R** (Mac)
- Or open page in Incognito/Private mode

---

## 📊 **Quick Reference: Pages to Keep**

| Calculator Name | URL Slug | Notes |
|----------------|----------|-------|
| **US Tax Calculator Suite** | `us-tax-calculator-suite` | Landing page |
| **Federal Income Tax Calculator** | `federal-income-tax-calculator` | Keep newest |
| **State Income Tax Calculator** | `state-income-tax-calculator` | Keep newest |
| **Capital Gains Tax Calculator** | `capital-gains-tax-calculator` | Keep newest |
| **Self-Employment Tax Calculator** | `self-employment-tax-calculator` | Keep newest |
| **Retirement Tax Calculator** | `retirement-tax-calculator` | Keep newest |
| **Tax Withholding Calculator** | `tax-withholding-calculator` | Keep NEW version |
| **Lump Sum Investment Calculator** | `lump-sum-investment-calculator` | Keep newest |
| **Retirement Planner and Estimator** | `retirement-planner-estimator` | ⭐ Update with fixed version |
| **SIP Calculator** | `sip-calculator` | Keep NEW version |
| **Compound Interest Calculator** | `compound-interest-calculator` | Keep newest |
| **Loan EMI Calculator** | `loan-emi-calculator` | Keep newest |

**Total Pages to Keep:** 12 unique calculator pages

---

## 🔍 **How to Check Page ID**

If you need to identify a page by its ID:

1. **Hover** over the page title in the Pages list
2. Look at your browser's status bar (bottom left)
3. You'll see a URL like: `post.php?post=3173&action=edit`
4. The number after `post=` is the page ID
5. **Alternative:** Click "Edit" and check the URL in your browser's address bar

---

## ⚠️ **Troubleshooting**

### **Problem: Can't find duplicate pages**
**Solution:**
- Use search box to search for "calculator", "retirement", "tax"
- Sort by Date to see recently created pages
- Check if duplicates are in Trash already

### **Problem: Page won't delete**
**Solution:**
- Check if page is set as Homepage (Settings → Reading)
- Check if page is in a menu (Appearance → Menus)
- Try logging out and back in
- Contact hosting support if issue persists

### **Problem: Retirement planner still looks broken**
**Solution:**
- Verify you're in Code/HTML editor mode (not Visual)
- Make sure you copied content from `retirement-planner-fixed.html`
- Clear all caches (WordPress + browser)
- Check browser console for JavaScript errors (F12)

### **Problem: Calculator not working after update**
**Solution:**
- Preview the page to test
- Check browser console for errors (F12)
- Verify JavaScript is enabled
- Check if any security plugin is blocking scripts
- Restore from Trash if needed

### **Problem: Too many pages to review**
**Solution:**
- Focus on calculator pages only
- Use search to filter: "calculator"
- Sort by date, focus on recent duplicates
- Take breaks, do in multiple sessions

---

## ✅ **Cleanup Completion Checklist**

After completing cleanup:

- [ ] All duplicate calculator pages identified
- [ ] Older/duplicate pages moved to Trash
- [ ] Only most recent version of each calculator kept
- [ ] Retirement planner updated with fixed version
- [ ] All 12 calculators tested and working
- [ ] No 404 errors on any calculator URL
- [ ] All caches cleared (WordPress + browser)
- [ ] Pages export backup created
- [ ] No JavaScript console errors
- [ ] Mobile responsive verified
- [ ] Trash reviewed (verify nothing important deleted)

---

## 📈 **Expected Results**

### **Before Cleanup:**
- Multiple duplicate pages
- Confusion about which version to use
- Possible broken functionality
- SEO issues (duplicate content)
- Difficult to maintain

### **After Cleanup:**
- 12 unique calculator pages (no duplicates)
- Clear, organized page list
- All calculators working perfectly
- Better SEO (no duplicate content)
- Easy to maintain
- Faster site (less content)

---

## 📞 **Need Help?**

If you encounter issues:

1. **Don't panic** - Pages in Trash can be restored
2. **Restore from backup** if needed (Tools → Import)
3. **Check documentation** - See WORDPRESS_CLEANUP_PLAN.md
4. **Review before permanent deletion** - Wait 24-48 hours
5. **Test in staging** if available

---

## 🎉 **Success!**

When you see:
- ✅ Only 12 unique calculator pages
- ✅ No duplicates in All Pages list
- ✅ All calculators working
- ✅ Retirement planner with all fixes
- ✅ Clean, organized admin panel

**Congratulations! Cleanup is complete!** 🎊

---

**Document Version:** 1.0  
**Created:** November 2, 2025  
**For:** SphereVista360 WordPress Admin
