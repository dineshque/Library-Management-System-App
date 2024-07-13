<template>
    <div class="container">
        <div class="row">
            <div class="col">
                <div class="card">
                    <div class="card-header">
                        <h4>User Registration</h4>
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="handleSubmit">
                            <div class="form-group">
                                <label>User Name</label>
                                <input type="text" v-model="username" class="form-control" placeholder="User Name"
                                    required>
                            </div>
                            <div class="form-group">
                                <label>Email</label>
                                <input type="email" v-model="email" class="form-control" placeholder="Email" required>
                            </div>
                            <div class="form-group">
                                <label>Password</label>
                                <input type="password" v-model="password" class="form-control" placeholder="Password"
                                    required>
                            </div>
                            <button type="submit" class="btn btn-primary btn-block">Register</button>
                            <h3>Login here with the same ID</h3>
                            <router-link to="/userLogin">Login here</router-link>
                        </form>
                        <h5 class='text-danger red-star'>{{ error }}</h5>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            username: '',
            email: '',
            password: '',
            error: null
        };
    },
    methods: {
        async handleSubmit() {
            const userData = {
                username: this.username,
                email: this.email,
                password: this.password,
                role: 'user'
            };

            try {
                const res = await fetch('http://localhost:5000/user-registration', {
                    method: 'post',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(userData),
                });
                const data = await res.json();
                if (res.ok) {
                    this.$router.push('/userlogin');
                } else {
                    this.error = data.message
                }
            } catch (error) {
                console.error('Error during login:', error);
            }

            this.username = '';
            this.email = '';
            this.password = '';
        }
    }
};
</script>


<style scoped>
.container {
    margin-top: 5;
    display: flex;
    justify-content: center;
}

.card {
    margin-top: 20%;
    background-color: rgb(213, 195, 171);
    width: 40rem;
}

input {
    background-color: bisque;
}

button {
    background-color: rgba(35, 65, 173, 0.918);
}
</style>