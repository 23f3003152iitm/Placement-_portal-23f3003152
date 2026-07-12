<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        
       
        <a class="navbar-brand" href="#">PlaceME..</a>

       
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

     
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            
            
            <li class="nav-item" >
              <router-link to="/"  class="btn btn-success ms-3">Home</router-link>
            </li>

            
            <li class="nav-item" style="margin: 1px; padding: 2px;">
              <button class="btn btn-danger ms-3" @click="logout">
                Logout
              </button>
            </li>

          </ul>
        </div>

      </div>
    </nav>

    <!-- Page Content -->
    <router-view />
  </div>
</template>



<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const logout = () => {
  // clear token / user data
  localStorage.removeItem('token')
  router.push('/')
}
</script>

<style>
body {
  margin: 0;
}
</style>
