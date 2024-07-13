<template>
    <div class="container d-flex justify-content-between">
        <img class="mt-4" :src="dist" width="700" height="600" alt="Pie Chart">
        <div class="d-flex align-items-end flex-column">
            <div class="card px-2 mt-4">
                <div class="card-header col-12">
                    <h4 style="color:darkred;"> Active Users </h4>
                    <span class="h3 mx-5" style="color:black;margin-left:4rem;">{{ stats.users }}</span>
                </div>
            </div>

            <div class="card px-2 my-5">
                <div class="card-header col-12">
                    <h4 style="color:darkred;"> Total Books </h4>
                    <span class="h3 mx-5" style="color:black;">{{ stats.books }}</span>
                </div>
            </div>

            <div class="card ">
                <div class="card-header col-12">
                    <h4 style="color:darkred;"> Total Sections </h4>
                    <span class="h3" style="color:black; margin-left:4rem;">{{ stats.sections }}</span>
                </div>
            </div>
        </div>

    </div>

</template>

<script>
import { mapGetters } from 'vuex';
export default {
    name: 'libStats',
    data() {
        return {
            authToken: localStorage.getItem('auth-token'),
            stats: [],
            dist: '',

        }
    },
    computed: {
        ...mapGetters(['alertMessage']),
    },
    methods: {
        clearAlert() {
            var alertMessage = null;
            this.$store.dispatch("updateAlert", alertMessage)
        },
        alertTimer() {
            setTimeout(() => {
                var alertMessage = null;
                this.$store.dispatch("updateAlert", alertMessage)
            }, 3500)
        },
        async loadStatsData() {
            try {
                var res = await fetch(`http://localhost:5000/api/stats`, {
                    headers: {
                        'Authentication-Token': this.authToken,
                    },
                })

                const data = await res.json()
                if (res.ok) {
                    this.stats = data
                }
                else {
                    var alertMessage = { "Notification": data.message };
                }
            } catch (error) {
                var alertMessage = { "Notification": error };
            }
            this.$store.dispatch('updateAlert', alertMessage);
            this.alertTimer();
        },
        async loadDistData() {
            try{
            var res = await fetch(`http://localhost:5000/api/dist`, {
                headers: {
                    'Authentication-Token': this.authToken,
                },
            })

            if (res.ok) {
                const data = await res.blob()
                this.dist = URL.createObjectURL(data);

                
            }
            else {
          var alertMessage = { "Notification": data.message };
        }
      } catch (error) {
        var alertMessage = { "Notification": error };
      }
      this.$store.dispatch('updateAlert', alertMessage);
      this.alertTimer();
        },
    },

    async mounted() {
        await this.loadStatsData();
        await this.loadDistData();
    },
};
</script>

<style scoped>
.card {
    border-radius: 1.5rem;
}
</style>