#!/usr/bin/env python3
"""Algebraically stabilize the C10.65r1 shadow B closure without changing its equations.

The original split phi=phi_A+phi_B B and the first reduced form both retain
cancellation-sensitive combinations at small k.  Here the same frozen
Hamiltonian+momentum system is reduced analytically using
Q=(C2*k^2-3*a^2*dm)/(3*H) and L=-k^2, so the common L factor cancels before
floating-point evaluation.  No threshold, state, RHS, or physical assumption is
changed.  The frozen B-denominator diagnostic normalization is preserved.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
pt=root/'source'/'perturbations.c'
s=pt.read_text()
marker='RTK_C10_65R1_CONDITIONED_B_CLOSURE_V2'
if marker in s:
    print('C10_65R1_CONDITIONED_B_CLOSURE_ALREADY_APPLIED')
    raise SystemExit(0)
old='''        r1_phiA=(-3.*r1_a*r1_a*r1_rr*r1_dm-r1_D*r1_H*r1_Q+2.*r1_D*r1_H*r1_psipA+2.*r1_rr*r1_Pcal*r1_L*r1_psi)/r1_lapse;
        r1_phiB=(2.*r1_D*r1_H*r1_psipB)/r1_lapse;
        r1_shift=r1_rr*r1_L;
        r1_Bden=r1_shift+r1_D*(r1_psipB+r1_H*r1_phiB);
        class_test(r1_Bden == 0.,error_message,"C10.65r1 B denominator vanished");
        r1_Brhs=r1_Q-r1_D*(r1_psipA+r1_H*r1_phiA);
        r1_B=r1_Brhs/r1_Bden;
        r1_psip=r1_psipA+r1_psipB*r1_B; r1_phi=r1_phiA+r1_phiB*r1_B;'''
new='''        /* RTK_C10_65R1_CONDITIONED_B_CLOSURE_V2
         * Exact algebraic reduction of the frozen Hamiltonian+momentum system.
         * Using Q=(C2*k^2-3*a^2*dm)/(3H) and L=-k^2, the common L factor
         * cancels before evaluation:
         *   B = [E(Q-D psipA)-D H C2-2D H P psi]
         *       / [lapse + D E psipB].
         * This removes the remaining O(1)-O(1) cancellation at low k.
         *
         * IMPORTANT: c10_65r1_B_den is a frozen diagnostic whose parent
         * semantics are the original finite-k denominator
         *   rr*L + D*(psipB + H*phiB).
         * After using the conditioned denominator internally, restore that
         * diagnostic in the algebraically equivalent, well-conditioned form
         *   rr*L*(lapse + D*E*psipB)/lapse.
         * This changes neither B nor any dynamics; it only preserves the
         * pre-frozen diagnostic definition across the numerical refactor. */
        r1_phiA=(-3.*r1_a*r1_a*r1_rr*r1_dm-r1_D*r1_H*r1_Q+2.*r1_D*r1_H*r1_psipA+2.*r1_rr*r1_Pcal*r1_L*r1_psi)/r1_lapse;
        r1_phiB=(2.*r1_D*r1_H*r1_psipB)/r1_lapse;
        r1_shift=r1_rr*r1_L;
        r1_Bden=r1_lapse+r1_D*r1_Eth*r1_psipB;
        class_test(r1_Bden == 0.,error_message,"C10.65r1 conditioned B denominator vanished");
        r1_Brhs=r1_Eth*(r1_Q-r1_D*r1_psipA)
                 -r1_D*r1_H*r1_C2
                 -2.*r1_D*r1_H*r1_Pcal*r1_psi;
        r1_B=r1_Brhs/r1_Bden;
        r1_Bden=r1_rr*r1_L*r1_Bden/r1_lapse;
        class_test(r1_Bden == 0.,error_message,"C10.65r1 frozen diagnostic B denominator vanished");
        r1_psip=r1_psipA+r1_psipB*r1_B;
        r1_phi=(-3.*r1_a*r1_a*r1_rr*r1_dm-r1_D*r1_H*r1_Q+2.*r1_D*r1_H*r1_psip+2.*r1_rr*r1_Pcal*r1_L*r1_psi)/r1_lapse;'''
if old not in s:
    # Allow upgrading a tree on which the V1 conditioned block has already been applied.
    old='''        /* RTK_C10_65R1_CONDITIONED_B_CLOSURE_V1
         * Algebraically identical reduction of Hamiltonian+momentum.  It avoids
         * subtracting O(1) terms to form the tiny finite-k B numerator/denominator.
         * With E=Eth and P=Pcal:
         * Bden = r L [1 + D E psipB/lapse]
         * Brhs = r/lapse [E L(Q-D psipA)+3D H^2 Q+3D H a^2 dm-2D H P L psi]. */
        r1_phiA=(-3.*r1_a*r1_a*r1_rr*r1_dm-r1_D*r1_H*r1_Q+2.*r1_D*r1_H*r1_psipA+2.*r1_rr*r1_Pcal*r1_L*r1_psi)/r1_lapse;
        r1_phiB=(2.*r1_D*r1_H*r1_psipB)/r1_lapse;
        r1_shift=r1_rr*r1_L;
        r1_Bden=r1_rr*r1_L*(1.+r1_D*r1_Eth*r1_psipB/r1_lapse);
        class_test(r1_Bden == 0.,error_message,"C10.65r1 conditioned B denominator vanished");
        r1_Brhs=(r1_rr/r1_lapse)*(r1_Eth*r1_L*(r1_Q-r1_D*r1_psipA)
                 +3.*r1_D*r1_H*r1_H*r1_Q
                 +3.*r1_D*r1_H*r1_a*r1_a*r1_dm
                 -2.*r1_D*r1_H*r1_Pcal*r1_L*r1_psi);
        r1_B=r1_Brhs/r1_Bden;
        r1_psip=r1_psipA+r1_psipB*r1_B;
        r1_phi=(-3.*r1_a*r1_a*r1_rr*r1_dm-r1_D*r1_H*r1_Q+2.*r1_D*r1_H*r1_psip+2.*r1_rr*r1_Pcal*r1_L*r1_psi)/r1_lapse;'''
if old not in s:
    raise SystemExit('C10.65r1 B closure block not found')
s=s.replace(old,new,1)
pt.write_text(s)
print('C10_65R1_CONDITIONED_B_CLOSURE_APPLIED')
