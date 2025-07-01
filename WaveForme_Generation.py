from params import *


logMc = float(sys.argv[1])  # primer argumento
q = float(sys.argv[2])      # segundo argumento
print(f"[Script] Recibí logMc = {logMc}, q = {q}")

print("riroriro start")
#Inspiral portion (inspiralfuns)
print("Inspiral portion calculation")
M, eta = ins.get_M_and_eta(logMc=logMc,q=q)
start_x = ins.startx(M,flow)
end_x = ins.endx(eta,merger_type)

x, xtimes, dt = ins.PN_parameter_integration(start_x,end_x,M,eta)
realtimes = ins.inspiral_time_conversion(xtimes,M)
i_phase, omega, freq = ins.inspiral_phase_freq_integration(x,dt,M)
r, rdot = ins.radius_calculation(x,M,eta)
A1, A2 = ins.a1_a2_calculation(r,rdot,omega,D,M,eta)
i_Aorth, i_Adiag = ins.inspiral_strain_polarisations(A1,A2,i_phase)
i_amp = ins.inspiral_strain_amplitude(i_Aorth,i_Adiag)


i_time = ins.list_size_reducer(100,realtimes)
i_omega = ins.list_size_reducer(100,omega)
i_phase = ins.list_size_reducer(100,i_phase)
i_amp = ins.list_size_reducer(100,i_amp)
i_Aorth = ins.list_size_reducer(100,i_Aorth)
i_Adiag = ins.list_size_reducer(100,i_Adiag)

#Starting the merger/ringdown portion (mergerfirstfuns)
print("Starting the merger/ringdown portion")
sfin, wqnm = me1.quasi_normal_modes(eta)
alpha, b, C, kappa = me1.gIRS_coefficients(eta,sfin)
fhat, m_omega = me1.merger_freq_calculation(wqnm,b,C,kappa)
fhatdot = me1.fhat_differentiation(fhat)
m_time = me1.merger_time_conversion(M)

#Matching the inspiral and merger/ringdown (matchingfuns)
print("Matching the inspiral and merger/ringdown portions")
min_switch_ind = mat.min_switch_ind_finder(i_time,i_omega,m_time,m_omega)

final_i_index = mat.final_i_index_finder(min_switch_ind,i_omega,m_omega)
time_offset = mat.time_offset_finder(min_switch_ind,final_i_index,i_time,m_time)
i_m_time, i_m_omega = mat.time_frequency_stitching(min_switch_ind,final_i_index,time_offset,i_time,i_omega,m_time,m_omega)
i_m_freq = mat.frequency_SI_units(i_m_omega,M)

#Rest of merger/ringdown functions (mergersecondfuns)
print("Rest of merger/ringdown functions")
m_phase = me2.merger_phase_calculation(min_switch_ind,final_i_index,i_phase,m_omega)
i_m_phase = me2.phase_stitching(final_i_index,i_phase,m_phase)
m_amp = me2.merger_strain_amplitude(min_switch_ind,final_i_index,alpha,i_amp,m_omega,fhat,fhatdot)
i_m_amp = me2.amplitude_stitching(final_i_index,i_amp,m_amp)

m_Aorth, m_Adiag = me2.merger_polarisations(final_i_index,m_amp,m_phase,i_Aorth)
i_m_Aorth, i_m_Adiag = me2.polarisation_stitching(final_i_index,i_Aorth,i_Adiag,m_Aorth,m_Adiag)

# Crear el DataFrame
print("Dowland Wave Forme")
df = pd.DataFrame({
    "time": i_m_time,
    "A_orth": i_m_Aorth,
    "A_diag": i_m_Adiag
})

# Guardar como CSV
df_str = path + "ondas_riroriro_logMc%s_q%s.csv"%(logMc,q)
print(f"The wave forme will be in {df_str}")
df.to_csv(df_str, index=False)


