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
  {
    path: "/",
    name: "Login",
    component: Login,
  },

  {
    path: "/register",
    name: "Register",
    component: Register,
  },






  {
    path: "/Admin_dash",
    name: "Admin Dashboard",
    component: Admin_dash,
  },
  {
    path: "/Admin_companies",
    name: "Admin Companies",
    component: Admin_companies,
  },
  {
    path: "/Admin_students",
    name: "Admin Students",
    component: Admin_students,


  },
  {
    path: "/Admin_drives",
    name: "Admin Drives",
    component: Admin_drives,

  },
  {
    path: "/Admin_applications",
    name: "Admin Applications",
    component: Admin_applications,
  },
  {
    path: "/Admin_searchs",
    name: "Admin Search",
    component: Admin_searchs,
  },



  {
    path: "/company_dash",
    name: "Company Dashboard",
    component: company_dash,
  },
  {
    path: "/company_profile",
    name: "Commpany Profile",
    component: Company_profile
  },
  {
    path: "/company_app",
    name: "Company Applications",
    component: company_app,
  },
  {
    path: "/company_create",
    name: "Company Create",
    component: company_create,
  },
  {
    path: "/company_drives",
    name: "Company Drives",
    component: company_drives,
  },
  {
    path: "/company_edit",
    name: "Company Edit",
    component: company_edit,
  },


  {
    path: "/student_dash",
    name: "Student Dashboard",
    component: student_dash,
  },
  {
    path: "/student_profile",
    name: "Student Profile",
    component: student_profile,
  },
  {
    path: "/student_applications",
    name: "Student Applications",
    component: student_applications,
  },
  {
    path: "/student_drives",
    name: "Student Drives",
    component: student_drive,
  },
  {
    path: "/student_edit",
    name: "Student Edit Profile",
    component: student_edit,
  },
  {
    path: "/student_history",
    name: "Student History",
    component: history,
  }

 
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router