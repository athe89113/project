<template>
  <user-list :company-id="companyId"></user-list>
</template>

<script>
  import userList from "../user/user-list.vue"
  export default {
    data: function () {
      return {
        companyId: this.$route.params.company_id
      }
    },
    ready: function () {
    },
    methods: {
    },
    components: {
      userList
    }
  }
</script>