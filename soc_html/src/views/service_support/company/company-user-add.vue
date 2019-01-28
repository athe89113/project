<template>
  <user-add-base :company-id="companyId"></user-add-base>
</template>

<script>
  import userAddBase from "../user/user-add-base.vue"
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
      userAddBase
    }
  }
</script>