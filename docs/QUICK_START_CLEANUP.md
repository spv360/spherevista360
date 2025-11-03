# QUICK START: WordPress Duplicate Cleanup

## ⚡ Fast Track (5 Minutes Read)

### ✅ What's Been Done
- 7 duplicate local files removed and backed up
- 12 production calculator files organized
- All documentation created
- Backup folder: `backup_old_versions_20251102_114437/`

### ⏳ What You Need to Do

**Goal:** Remove duplicate pages from WordPress admin

**Time:** 20-30 minutes

**Steps:**

1. **Backup** (2 min)
   ```
   WordPress Admin → Tools → Export → Pages → Download
   ```

2. **Find Duplicates** (5 min)
   ```
   Pages → All Pages → Sort by Title
   Look for: Same names, numbered slugs (-2, -3), test pages
   ```

3. **Delete Duplicates** (10 min)
   ```
   For each duplicate set:
   - Keep the NEWEST (check Modified date)
   - Trash all OLDER versions
   - Hover over page → Click "Trash"
   ```

4. **Update Retirement Planner** (5 min) ⭐ IMPORTANT
   ```
   - Edit page ID 3173
   - Switch to Code editor
   - Copy from: retirement-planner-fixed.html
   - Paste and Update
   - Delete page 3217 if exists
   ```

5. **Test** (5 min)
   ```
   Visit each calculator URL
   Test calculations work
   Check mobile view
   ```

6. **Clear Cache** (2 min)
   ```
   bash clear_cache.sh
   OR
   WP-Optimize → Purge Cache
   ```

7. **Verify** (1 min)
   ```
   Confirm: 12 unique calculator pages
   No duplicates in All Pages list
   ```

---

## 📚 Full Documentation

- **WORDPRESS_ADMIN_CLEANUP_GUIDE.md** - Detailed step-by-step
- **WORDPRESS_CLEANUP_PLAN.md** - Complete strategy
- **CLEANUP_SUMMARY.md** - Full summary

---

## 🎯 12 Pages to Keep

1. US Tax Calculator Suite (landing)
2. Federal Income Tax Calculator
3. State Income Tax Calculator
4. Capital Gains Tax Calculator
5. Self-Employment Tax Calculator
6. Retirement Tax Calculator
7. Tax Withholding Calculator (NEW version)
8. Lump Sum Investment Calculator
9. Retirement Planner and Estimator (UPDATE with fixed version)
10. SIP Calculator (NEW version)
11. Compound Interest Calculator
12. Loan EMI Calculator

**Delete:** All duplicates, numbered versions (-2, -3), test pages

---

## ⚠️ Known Duplicate

- **Delete:** Page ID 3217 "Retirement Planner and Estimator"
- **Keep & Update:** Page ID 3173 "Retirement Planner and Estimator"

---

## 🛡️ Safety

- ✅ All local files backed up
- ✅ WordPress pages go to Trash (not deleted permanently)
- ✅ Can restore within 30 days
- ✅ Export backup before starting

---

## 📞 Help

**Problem:** Can't find duplicates
**Solution:** Search "calculator" in Pages → All Pages

**Problem:** Retirement planner still broken
**Solution:** Use Code editor (not Visual), copy from retirement-planner-fixed.html

**Problem:** Calculator not working
**Solution:** Check browser console (F12), clear all caches

**Full Guide:** See WORDPRESS_ADMIN_CLEANUP_GUIDE.md

---

## ✅ Success Checklist

- [ ] Backup created (Tools → Export)
- [ ] Duplicates identified
- [ ] Old versions trashed
- [ ] Retirement planner updated (page 3173)
- [ ] All 12 calculators tested
- [ ] Cache cleared
- [ ] No duplicates remain
- [ ] All URLs working

---

**Ready?** Start with: WORDPRESS_ADMIN_CLEANUP_GUIDE.md

**Quick Reference:** This file

**Full Details:** CLEANUP_SUMMARY.md
