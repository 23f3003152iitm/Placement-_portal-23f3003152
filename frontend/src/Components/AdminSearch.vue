<template>
  <div class="container mt-5" style="max-width: 860px;">
    <h2 class="mb-4 text-center">Search</h2>

    <div v-if="errorMessage" class="alert alert-danger alert-dismissible">
      {{ errorMessage }}
      <button type="button" class="btn-close" @click="errorMessage = ''"></button>
    </div>

    <div class="border rounded-3 shadow-sm p-4 mb-4">
      <div class="mb-3">
        <label class="form-label fw-semibold">Search In</label>
        <div class="d-flex gap-3">
          <div class="form-check">
            <input class="form-check-input" type="radio" id="searchStudents" value="students" v-model="searchType" />
            <label class="form-check-label" for="searchStudents">Students</label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="radio" id="searchCompanies" value="companies" v-model="searchType" />
            <label class="form-check-label" for="searchCompanies">Companies</label>
          </div>
        </div>
      </div>

      <div class="mb-3">
        <label for="query" class="form-label fw-semibold">
          {{ searchType === "students" ? "Search by Name" : "Search by Company Name" }}
        </label>
        <div class="input-group">
          <input
            type="text"
            class="form-control"
            id="query"
            v-model="query"
            :placeholder="searchType === 'students' ? 'Enter student name...' : 'Enter company name...'"
            @keyup.enter="handleSearch"
          />
          <button class="btn btn-primary" @click="handleSearch" :disabled="isSearching || !query.trim()">
            <span v-if="isSearching" class="spinner-border spinner-border-sm me-2"></span>
            Search
          </button>
        </div>
      </div>
    </div>

    <div v-if="searchType === 'students' && results.length > 0">
      <h5 class="mb-3 text-muted">
        Student Results <span class="badge bg-primary ms-2">{{ results.length }}</span>
      </h5>
      <div class="border rounded-3 shadow-sm p-3 overflow-auto">
        <table class="table table-bordered table-hover align-middle">
          <thead class="table-light">
            <tr><th>#</th><th>Name</th><th>Email</th><th>Branch</th></tr>
          </thead>
          <tbody>
            <tr v-for="(s, index) in results" :key="s.id">
              <td>{{ index + 1 }}</td><td>{{ s.name }}</td><td>{{ s.email }}</td><td>{{ s.branch }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="searchType === 'companies' && results.length > 0">
      <h5 class="mb-3 text-muted">
        Company Results <span class="badge bg-success ms-2">{{ results.length }}</span>
      </h5>
      <div class="border rounded-3 shadow-sm p-3 overflow-auto">
        <table class="table table-bordered table-hover align-middle">
          <thead class="table-light">
            <tr><th>#</th><th>Company Name</th><th>Website</th><th>Status</th></tr>
          </thead>
          <tbody>
            <tr v-for="(c, index) in results" :key="c.id">
              <td>{{ index + 1 }}</td>
              <td>{{ c.company_name }}</td>
              <td><a :href="c.website" target="_blank" rel="noopener">{{ c.website }}</a></td>
              <td><span :class="statusBadge(c.approval_status)">{{ c.approval_status }}</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="searched && results.length === 0" class="text-center text-muted py-4">
      No results found for "<strong>{{ lastQuery }}</strong>".
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AdminSearch",
  data() {
    return {
      searchType: "students",
      query: "",
      results: [],
      isSearching: false,
      searched: false,
      lastQuery: "",
      errorMessage: "",
    };
  },
  watch: {
    searchType() {
      this.results = [];
      this.searched = false;
      this.query = "";
    },
  },
  methods: {
    async handleSearch() {
      if (!this.query.trim()) return;
      this.isSearching = true;
      this.errorMessage = "";
      this.results = [];
      const token = localStorage.getItem("token");
      this.lastQuery = this.query;
      const endpoint = this.searchType === "students"
        ? "http://localhost:5000/api/admin/search/students"
        : "http://localhost:5000/api/admin/search/companies";
      try {
        const res = await axios.get(endpoint, {
          params: { query: this.query },
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.results = res.data;
        this.searched = true;
      } catch (err) {
        if (err.response?.status === 401) {
          localStorage.clear();
          this.$router.push("/login");
        } else {
          this.errorMessage = "Search failed. Please try again.";
        }
      } finally {
        this.isSearching = false;
      }
    },

    statusBadge(status) {
      const map = { Approved: "badge bg-success", Rejected: "badge bg-danger", Pending: "badge bg-warning text-dark" };
      return map[status] || "badge bg-secondary";
    },
  },
};
</script>
