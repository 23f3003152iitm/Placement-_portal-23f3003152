import { defineStore } from "pinia"

const API = "http://localhost:5000"

export const useUserStore = defineStore("user", {
  state: () => ({
    token: localStorage.getItem("token") || null
  }),


  actions: {
  async login(email, password) {

    localStorage.clear()  // wipe all previous user's data



    const res = await fetch(`${API}/login`, {  // ← also fix URL (missing /api)
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    })

    const data = await res.json()

    if (!res.ok) throw new Error(data.message) 

    console.log("Full response data:", data)
    console.log("Role:", data.role)
    console.log("Role lowercase:", data.role.toLowerCase())
    console.log("Is student?:", data.role.toLowerCase() === "student")

    this.token = data.token
    localStorage.setItem("token", data.token)
    localStorage.setItem("id", data.id)         
    localStorage.setItem("role", data.role)     
    localStorage.setItem("email", data.email)   


    
if (data.role.toLowerCase() === "student") {
  console.log("Token being sent:", data.token)  // ← add this
  // const check = await fetch(`${API}/api/student/check/${data.id}`, {
  //   method: "GET",                               // ← add method explicitly
  //   headers: {
  //     "Content-Type": "application/json",        // ← add this
  //     Authorization: `Bearer ${data.token}`
  //   }


  const check = await fetch(`${API}/api/student/check/${data.id}`, {
  method: "GET",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${data.token}`
  }
})
  console.log("Check status:", check.status)
  const checkData = await check.json()
  console.log("Check response:", checkData)  // ← what does Flask return?
    


  if (checkData.exists) {
    localStorage.setItem("student_id", checkData.student_id)
  }
}

if (data.role.toLowerCase() === "company") {
  console.log("Checking if company exists in backend...")
  const check = await fetch(`${API}/api/company/check/${data.id}`, {
    headers: {
      Authorization: `Bearer ${data.token}`  // ← add token here
    }
  })
  const checkData = await check.json()
  console.log("Check data:", checkData)

  if (checkData.exists) {
    localStorage.setItem("company_id", checkData.company_id)
  }
}

    
    return data   
  },

  logout() {
    this.token = null
    localStorage.removeItem("token")
    localStorage.removeItem("id")      
    localStorage.removeItem("role")
    localStorage.removeItem("email")
    localStorage.removeItem("student_id")
    localStorage.removeItem("company_id")
  }
}




})
