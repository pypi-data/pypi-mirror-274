#ifndef RWWEX_HPP
#define RWWEX_HPP
#include "cubnm/models/base.hpp"
class rWWExModel : public BaseModel {
public:
    using BaseModel::BaseModel;
    ~rWWExModel() {
        if (cpu_initialized) {
            this->free_cpu();
        }
        #ifdef _GPU_ENABLED
        if (gpu_initialized) {
            this->free_gpu();
        }
        #endif
    }

    static constexpr char *name = "rWWEx";
    static constexpr int n_state_vars = 3; // number of state variables (u_real)
    static constexpr int n_intermediate_vars = 2; // number of intermediate/extra u_real variables
    static constexpr int n_noise = 1; // number of noise elements needed for each node
    static constexpr int n_global_params = 1; // G
    static constexpr int n_regional_params = 3; // w, I0, sigma
    // static constexpr char* state_var_names[] = {"x", "r", "S"};
    // static constexpr char* intermediate_var_names[] = {"axb", "dSdt"};
    // static constexpr char* conn_state_var_name = "S"; // name of the state variable which sends input to connected nodes
    static constexpr int conn_state_var_idx = 2;
    // static constexpr char* bold_state_var_name = "S"; // name of the state variable which is used for BOLD calculation
    static constexpr int bold_state_var_idx = 2;
    // the following are needed for numerical FIC
    static constexpr int n_ext_int = 0; // number of additional int variables for each node
    static constexpr int n_ext_bool = 0; // number of additional bool variables for each node
    static constexpr int n_ext_int_shared = 0; // number of additional int variables shared
    static constexpr int n_ext_bool_shared = 0; // number of additional bool variables shared
    static constexpr int n_ext_u_real_shared = 0; // number of additional float/double variables shared
    static constexpr int n_global_out_int = 0;
    static constexpr int n_global_out_bool = 0;
    static constexpr int n_global_out_u_real = 0;
    static constexpr int n_regional_out_int = 0;
    static constexpr int n_regional_out_bool = 0;
    static constexpr int n_regional_out_u_real = 0;
    static constexpr bool has_post_bw_step = false;
    static constexpr bool has_post_integration = false;

    struct Constants {
        u_real dt;
        u_real sqrt_dt;
        u_real J_N;
        u_real a;
        u_real b;
        u_real d;
        u_real gamma;
        u_real tau;
        u_real itau;
        u_real dt_itau;
        u_real dt_gamma;
    };

    struct Config {
    };

    static Constants mc;
    Config conf;

    static void init_constants();

    // in set_conf we have nothing to add beyond BaseModel
    // void set_conf(std::map<std::string, std::string> config_map) override;

    #ifdef _GPU_ENABLED
    CUDA_CALLABLE_MEMBER void init(
        u_real* _state_vars, u_real* _intermediate_vars, 
        int* _ext_int, bool* _ext_bool,
        int* _ext_int_shared, bool* _ext_bool_shared
    );
    CUDA_CALLABLE_MEMBER void step(
        u_real* _state_vars, u_real* _intermediate_vars,
        u_real* _global_params, u_real* _regional_params,
        u_real& tmp_globalinput,
        u_real* noise, long& noise_idx
    );
    CUDA_CALLABLE_MEMBER void post_bw_step(
        u_real* _state_vars, u_real* _intermediate_vars,
        int* _ext_int, bool* _ext_bool, 
        int* _ext_int_shared, bool* _ext_bool_shared,
        bool& restart,
        u_real* _global_params, u_real* _regional_params,
        int& ts_bold
    ); // does nothing
    CUDA_CALLABLE_MEMBER void restart(
        u_real* _state_vars, u_real* _intermediate_vars, 
        int* _ext_int, bool* _ext_bool,
        int* _ext_int_shared, bool* _ext_bool_shared
    );
    CUDA_CALLABLE_MEMBER void post_integration(
        u_real ***state_vars_out, 
        int **global_out_int, bool **global_out_bool,
        u_real* _state_vars, u_real* _intermediate_vars, 
        int* _ext_int, bool* _ext_bool, 
        int* _ext_int_shared, bool* _ext_bool_shared,
        u_real** global_params, u_real** regional_params,
        u_real* _global_params, u_real* _regional_params,
        int& sim_idx, const int& nodes, int& j
    ); // does nothing

    void init_gpu(BWConstants bwc) override final {
        _init_gpu<rWWExModel>(this, bwc);
    }

    void run_simulations_gpu(
        double * BOLD_ex_out, double * fc_trils_out, double * fcd_trils_out,
        u_real ** global_params, u_real ** regional_params, u_real * v_list,
        u_real ** SC, int * SC_indices, u_real * SC_dist
    ) override final {
        _run_simulations_gpu<rWWExModel>(
            BOLD_ex_out, fc_trils_out, fcd_trils_out, 
            global_params, regional_params, v_list,
            SC, SC_indices, SC_dist, this
        );
    }
    #endif

    void h_init(
        u_real* _state_vars, u_real* _intermediate_vars, 
        int* _ext_int, bool* _ext_bool,
        int* _ext_int_shared, bool* _ext_bool_shared
    ) override final;
    void h_step(
        u_real* _state_vars, u_real* _intermediate_vars,
        u_real* _global_params, u_real* _regional_params,
        u_real& tmp_globalinput,
        u_real* noise, long& noise_idx
    ) override final;
    void _j_restart(
        u_real* _state_vars, u_real* _intermediate_vars, 
        int* _ext_int, bool* _ext_bool,
        int* _ext_int_shared, bool* _ext_bool_shared
    ) override final;


    void init_cpu() override final {
        _init_cpu<rWWExModel>(this);
    }

    void run_simulations_cpu(
        double * BOLD_ex_out, double * fc_trils_out, double * fcd_trils_out,
        u_real ** global_params, u_real ** regional_params, u_real * v_list,
        u_real ** SC, int * SC_indices, u_real * SC_dist
    ) override final {
        _run_simulations_cpu<rWWExModel>(
            BOLD_ex_out, fc_trils_out, fcd_trils_out, 
            global_params, regional_params, v_list,
            SC, SC_indices, SC_dist, this
        );
    }

    int get_n_state_vars() override final {
        return n_state_vars;
    }
    int get_n_global_out_bool() override final {
        return n_global_out_bool;
    }
    int get_n_global_out_int() override final {
        return n_global_out_int;
    }
    int get_n_global_params() override final {
        return n_global_params;
    }
    int get_n_regional_params() override final {
        return n_regional_params;
    }
    char * get_name() override final {
        return name;
    }
};

#endif
