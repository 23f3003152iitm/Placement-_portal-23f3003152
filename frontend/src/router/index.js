import { createRouter, createWebHistory } from "vue-router"

import Login from "../Components/login.vue"
import Register from "../Components/register.vue"

import Admin_dash from "../Components/AdminDashboard.vue"
import Admin_companies from "../Components/AdminCompanies.vue"
import Admin_students from "../Components/AdminStudents.vue"
import Admin_drives from "../Components/AdminDrives.vue"
import Admin_applications from "../Components/AdminApplications.vue" 
import Admin_searchs from "../Components/AdminSearch.vue"

import company_dash from "../Components/CompanyDashboard.vue"
import company_app from "../Components/CompanyApplications.vue"
import company_create from "../Components/CompanyCreate.vue"
import company_drives from "../Components/CompanyDrives.vue"
import company_edit from "../Components/CompanyEdit.vue"
import Company_profile from "../Components/CompanyProfile.vue"

import student_dash from "../Components/StudentDashboard.vue"
import student_profile from "../Components/StudentProfile.vue"
import student_applications from "../Components/StudentApplications.vue"
import student_edit from "../Components/StudentEditProfile.vue"
import student_drive from "../Components/StudentDrives.vue"
import history from "../Components/StudentHistory.vue"

const routes = [
  // ── Public routes (no login needed) ──
  { path: "/", name: "Login", component: Login },
  { path: "/register", name: "Register", component: Register },

  // ── Admin routes ──
  { path: "/Admin_dash", name: "Admin Dashboard",
     component: Admin_dash,
      meta: { requiresAuth: true, role: "admin" } },

  { path: "/Admin_companies", name: "Admin Companies",
    component: Admin_companies,
     meta: { requiresAuth: true, role: "admin" } },

  { path: "/Admin_students", name: "Admin Students",
    component: Admin_students,
     meta: { requiresAuth: true, role: "admin" } },

  { path: "/Admin_drives", name: "Admin Drives",
    component: Admin_drives,
     meta: { requiresAuth: true, role: "admin" } },

  { path: "/Admin_applications", name: "Admin Applications",
    component: Admin_applications,
     meta: { requiresAuth: true, role: "admin" } },

  { path: "/Admin_searchs", name: "Admin Search",
    component: Admin_searchs,
     meta: { requiresAuth: true, role: "admin" } },



  // ── Company routes ──

  { path: "/company_dash", name: "Company Dashboard",
    component: company_dash,
     meta: { requiresAuth: true, role: "company" } },

  { path: "/company_app", name: "Company Applications",
    component: company_app,
     meta: { requiresAuth: true, role: "company" } },

  { path: "/company_create", name: "Company Create",
    component: company_create,
     meta: { requiresAuth: true, role: "company" } },

  { path: "/company_drives", name: "Company Drives",
    component: company_drives,
     meta: { requiresAuth: true, role: "company" } },

  { path: "/company_edit", name: "Company Edit",
    component: company_edit,
     meta: { requiresAuth: true, role: "company" } },

  { path: "/Company_profile", name: "Company Profile",
    component: Company_profile,
     },



  // ── Student routes ──

  { path: "/student_profile", name: "Student Profile",
    component: student_profile, 
  },

  {path: "/student_dash", name: "Student Dashboard",
    component: student_dash,
     meta: { requiresAuth: true, role: "student" } },

  { path: "/student_applications", name: "Student Applications",
    component: student_applications,
     meta: { requiresAuth: true, role: "student" } },

  { path: "/student_edit", name: "Student Edit",
    component: student_edit,
     meta: { requiresAuth: true, role: "student" } },

  { path: "/student_drives", name: "Student Drives",
    component: student_drive,
     meta: { requiresAuth: true, role: "student" } },

  { path: "/student_history", name: "Student History",
    component: history,
     meta: { requiresAuth: true, role: "student" } },

]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// ── Navigation Guard ──
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token")
  const role = localStorage.getItem("role")

  if (to.meta.requiresAuth) {
    // No token → go to login
    if (!token) {
      next("/")
      return
    }

    // Wrong role → go to login
    // e.g. student trying to access /Admin_dash
    if (to.meta.role && role?.toLowerCase() !== to.meta.role.toLowerCase()) {
      next("/")
      return
    }

    // Token exists + correct role → allow
    next()

  } else {
    // Public route → allow
    next()
  }
})

export default router