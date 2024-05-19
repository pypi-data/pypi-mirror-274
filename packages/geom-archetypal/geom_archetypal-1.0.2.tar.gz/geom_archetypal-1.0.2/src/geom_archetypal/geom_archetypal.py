

import numpy as np
from scipy.sparse import csr_matrix
from datetime import datetime as dt
import itertools
import pandas as pd
from numpy.matlib import repmat
import time



def archetypal_pcha(df, kappas, conv_crit=1E-6, maxiter=2000, verbose=False):
    """
    Performs PCHA Archetypal Analysis:
    Given the data matrix df (n x d) and the number of archetypes kappas
    then two stochastic A (n x kappas) and B (kappas x n) matrices are computed such that
                             Y ~ ABY
    under the common Euclidean matrix norm.
    The matrix BY (kappas x d) is the matrix with kappas rows being the archetypes.
    For that purpose it is used a simplified and modified version of package "py_pcha":
    https://github.com/ulfaslak/py_pcha
    and at the PyPI:
    https://pypi.org/project/py-pcha/
    under next definitions:
    X=Y.T
    C=B.T
    S=A.T
    The original PCHA method is descibed at:
    Morup, M., Hansen, LK (2012) <doi:10.1016/j.neucom.2011.06.033>

    Input arguments
    ----------------
    df : numpy.2darray
        Data matrix (n x d)

    kappas : int
        Number of desired archetypes

    conv_crit : float
        The convergence criterion for stopping algorithm: stop if
        |SSE_9i+1)-SSE_i| / SSE_i < conv_crit

    maxiter : int
        The maximum number of iterations to be done

    verbose : bool
        Set True if running details should be printed

    Output results
    --------------

    BY : numpy.2darray
        (kappas x d) matrix of final archetypes: each row is d-dimensional vector

    A : numpy.2darray
        n x kappas matrix, positive and row stochastic

    B : numpy.2darray
        kappas x n matrix, positive and column stochastic

    SSE : float
        Sum of Squared Errors

    varexlp : float
        Percent variation explained by the PCHA

    BY0 : numpy.2darray
        (kappas x d) matrix of initial archetypes, as it was found by FurthestSum algorithm

    converges : bool
        Set True if algorithm has converged inside the given 'maxiter' iterations

    iterations : int
        Number of total iterations done by the main PCHA algorithm

    time : float
        The total elapsed time in seconds
    """
    total_time_1 = dt.now()
    delta = 0
    # Proceed to "py_pcha" entities:
    X = df.T
    if verbose:
        print()
        print('PCHA Archetypal Analysis:')
        print()
    # Define main update functions

    def s_update(S, XCtX, CtXtXC, muS, SST, SSE, niter):
        """Update S for one iteration of the algorithm."""
        kappas, J = S.shape
        e = np.ones((kappas, 1))
        for k in range(niter):
            SSE_old = SSE
            g = (np.dot(CtXtXC, S) - XCtX) / (SST / J)
            g = g - e * np.sum(g.A * S.A, axis=0)

            S_old = S
            while True:
                S = (S_old - g * muS).clip(min=0)
                S = S / np.dot(e, np.sum(S, axis=0))
                SSt = S * S.T
                SSE = SST - 2 * np.sum(XCtX.A * S.A) + np.sum(CtXtXC.A * SSt.A)
                if SSE <= SSE_old * (1 + 1e-9):
                    muS = muS * 1.2
                    break
                else:
                    muS = muS / 2

        return S, SSE, muS, SSt

    def c_update(X, XSt, XC, SSt, C, delta, muC, mualpha, SST, SSE, niter=1):
        """Update C for one iteration of the algorithm."""
        J, nos = C.shape

        if delta != 0:
            alphaC = np.sum(C, axis=0).A[0]
            C = np.dot(C, np.diag(1 / alphaC))

        e = np.ones((J, 1))
        XtXSt = np.dot(X.T, XSt)

        for k in range(niter):

            # Update C
            SSE_old = SSE
            g = (np.dot(X.T, np.dot(XC, SSt)) - XtXSt) / SST

            if delta != 0:
                g = np.dot(g, np.diag(alphaC))
            g = g.A - e * np.sum(g.A * C.A, axis=0)

            C_old = C
            while True:
                C = (C_old - muC * g).clip(min=0)
                nC = np.sum(C, axis=0) + np.finfo(float).eps
                C = np.dot(C, np.diag(1 / nC.A[0]))

                if delta != 0:
                    Ct = C * np.diag(alphaC)
                else:
                    Ct = C

                XC = np.dot(X, Ct)
                CtXtXC = np.dot(XC.T, XC)
                SSE = SST - 2 * np.sum(XC.A * XSt.A) + np.sum(CtXtXC.A * SSt.A)

                if SSE <= SSE_old * (1 + 1e-9):
                    muC = muC * 1.2
                    break
                else:
                    muC = muC / 2

            # Update alphaC
            SSE_old = SSE
            if delta != 0:
                g = (np.diag(CtXtXC * SSt).T / alphaC - np.sum(C.A * XtXSt.A)) / (SST * J)
                alphaC_old = alphaC
                while True:
                    alphaC = alphaC_old - mualpha * g
                    alphaC[alphaC < 1 - delta] = 1 - delta
                    alphaC[alphaC > 1 + delta] = 1 + delta

                    XCt = np.dot(XC, np.diag(alphaC / alphaC_old))
                    CtXtXC = np.dot(XCt.T, XCt)
                    SSE = SST - 2 * np.sum(XCt.A * XSt.A) + np.sum(CtXtXC.A * SSt.A)

                    if SSE <= SSE_old * (1 + 1e-9):
                        mualpha = mualpha * 1.2
                        XC = XCt
                        break
                    else:
                        mualpha = mualpha / 2

        if delta != 0:
            C = C * np.diag(alphaC)

        return C, SSE, muC, mualpha, CtXtXC, XC

    # Define furthestsum function:

    def furthest_sum(K, noc, i):
        """
        Furthest sum algorithm, to efficiently generate initial seed/archetypes.
        Taken from the package "py_pcha":
        https://github.com/ulfaslak/py_pcha
        and at the PyPI:
        https://pypi.org/project/py-pcha/
        Note: Commonly data is formatted to have shape (examples, dimensions).
        This function takes input and returns output of the transposed shape,
        (dimensions, examples).

        Parameters
        ----------
        K : numpy 2d-array
            Either a data matrix or a kernel matrix.

        noc : int
            Number of candidate archetypes to extract.

        i : int
            initial observation used for to generate the FurthestSum.

        exclude : numpy.1darray
            Entries in K that can not be used as candidates.

        Output
        ------
        i : int
            The extracted candidate archetypes
        """

        def max_ind_val(l):
            return max(zip(range(len(l)), l), key=lambda x: x[1])

        I, J = K.shape
        index = np.array(range(J))
        # index[exclude] = 0
        index[i] = -1
        ind_t = i
        sum_dist = np.zeros((1, J), np.complex128)

        if J > noc * I:
            Kt = K
            Kt2 = np.sum(Kt ** 2, axis=0)
            for k in range(1, noc + 11):
                if k > noc - 1:
                    Kq = np.dot(Kt[:, i[0]], Kt)
                    sum_dist -= np.lib.scimath.sqrt(Kt2 - 2 * Kq + Kt2[i[0]])
                    index[i[0]] = i[0]
                    i = i[1:]
                t = np.where(index != -1)[0]
                Kq = np.dot(Kt[:, ind_t].T, Kt)
                sum_dist += np.lib.scimath.sqrt(Kt2 - 2 * Kq + Kt2[ind_t])
                ind, val = max_ind_val(sum_dist[:, t][0].real)
                ind_t = t[ind]
                i.append(ind_t)
                index[ind_t] = -1
        else:
            if I != J or np.sum(K - K.T) != 0:  # Generate kernel if K not one
                Kt = K
                K = np.dot(Kt.T, Kt)
                K = np.lib.scimath.sqrt(
                    repmat(np.diag(K), J, 1) - 2 * K + \
                    repmat(np.mat(np.diag(K)).T, 1, J)
                )

            Kt2 = np.diag(K)  # Horizontal
            for k in range(1, noc + 11):
                if k > noc - 1:
                    sum_dist -= np.lib.scimath.sqrt(Kt2 - 2 * K[i[0], :] + Kt2[i[0]])
                    index[i[0]] = i[0]
                    i = i[1:]
                t = np.where(index != -1)[0]
                sum_dist += np.lib.scimath.sqrt(Kt2 - 2 * K[ind_t, :] + Kt2[ind_t])
                ind, val = max_ind_val(sum_dist[:, t][0].real)
                ind_t = t[ind]
                i.append(ind_t)
                index[ind_t] = -1

        return i

    # Get matrix dimensions
    N, M = X.shape
    # Compute the total sum of squares
    SST = np.sum(X * X)
    # Initialize matrix C which will define the archetypes:
    try:
        i = furthest_sum(X, kappas, [int(np.ceil(M * np.random.rand()))])
    except IndexError:
        class InitializationException(Exception):
            pass
        raise InitializationException("Initialization does not converge. Too few examples in dataset.")
    j = range(kappas)
    C = csr_matrix((np.ones(len(i)), (i, j)), shape=(M, kappas)).todense()
    # Define the initial solution:
    XC = np.dot(X, C)
    # Store the initial solution:
    BY0 = XC.T
    # Define initial values of mus parameters:
    muS, muC, mualpha = 1, 1, 1
    # Initialise S matrix:
    XCtX = np.dot(XC.T, X)
    CtXtXC = np.dot(XC.T, XC)
    S = -np.log(np.random.random((kappas, M)))
    S = S / np.dot(np.ones((kappas, 1)), np.mat(np.sum(S, axis=0)))
    SSt = np.dot(S, S.T)
    SSE = SST - 2 * np.sum(XCtX.A * S.A) + np.sum(CtXtXC.A * SSt.A)
    # Update the S matrix for a total of 25 iterations
    S, SSE, muS, SSt = s_update(S, XCtX, CtXtXC, muS, SST, SSE, 25)
    # Set PCHA parameters
    iterations = 0
    dSSE = np.inf
    varexpl = (SST - SSE) / SST
    if verbose:
        print('Principal Convex Hull Analysis / Archetypal Analysis')
        print('The mumber of Archetypes will be kappas = ' + str(kappas))
        print('To stop algorithm press control C\n')
    dheader = '%10s | %10s | %10s | %10s | %10s | %10s | %10s | %10s' % (
    'Iter', 'VarExpl', ' SSE ', '|dSSE|/SSE ', 'muC', 'mualpha', 'muS', ' Time(s)   ')
    dline = '|----------|------------|------------|-------------|------------|------------|------------|------------|'
    # Main iteration begins ...
    while np.abs(dSSE) >= conv_crit * np.abs(SSE) and iterations < maxiter and varexpl < 0.9999:
        if verbose and iterations % 100 == 0:
            print(dline)
            print(dheader)
            print(dline)
        told = dt.now()
        iterations += 1
        SSE_old = SSE

        # C (and alpha) update
        XSt = np.dot(X, S.T)
        C, SSE, muC, mualpha, CtXtXC, XC = c_update(
            X, XSt, XC, SSt, C, delta, muC, mualpha, SST, SSE, 10
        )

        # S update
        XCtX = np.dot(XC.T, X)
        S, SSE, muS, SSt = s_update(
            S, XCtX, CtXtXC, muS, SST, SSE, 10
        )

        # Evaluate and display iteration
        dSSE = SSE_old - SSE
        tnew = dt.now()
        if iterations % 1 == 0:
            time.sleep(0.000001)
            varexpl = (SST - SSE) / SST
            if verbose:
                print('|% 9.0f | %10.6f | %10.4e | %11.4e | %10.3e | %10.3e | %10.3e | %10.3f | ' % (
                iterations, varexpl, SSE, dSSE / np.abs(SSE), muC, mualpha, muS, 1e-6*(tnew - told).microseconds))

    # Display final iteration
    varexpl = (SST - SSE) / SST
    if verbose:
        print(dline)
        print('|% 9.0f | %10.6f | %10.4e | %11.4e | %10.3e | %10.3e | %10.3e | %10.3f | ' % (
        iterations, varexpl, SSE, dSSE / np.abs(SSE), muC, mualpha, muS, 1e-6*(tnew - told).microseconds))
        print(dline)

    # Sort components according to importance
    ind, vals = zip(
        *sorted(enumerate(np.sum(S, axis=1)), key=lambda x: x[0], reverse=1)
    )
    S = S[ind, :]
    C = C[:, ind]
    XC = XC[:, ind]
    if iterations == maxiter:
        converges = False
    else:
        converges = True
    # Convert to the convenient data frame terminology...
    BY = XC.T
    B = C.T
    A = S.T
    # Total ellapsed time:
    total_time_2 = dt.now()
    # total_time = 1e-6*(total_time_2 - total_time_1).microseconds
    total_time = (total_time_2 - total_time_1).seconds
    # Return ...
    return BY, A, B, SSE, varexpl, BY0, converges, iterations, total_time

#
#######################
#

def fast_archetypal(Y, irows, diag_less = 1e-2, verbose=False):
    """Performs Fast Archetypal Analysis:
    Given the kappas archetypes as the irows (kappas) rows of the data matrix Y (n x d)
    then the stochastic A (n x kappas) matrix is computed such that
                             Y ~ ABY
    under the common Euclidean matrix norm.

    For that purpose the code of package "py_pcha":
    https://github.com/ulfaslak/py_pcha
    is used, under next definitions:
    X=Y.T
    C=B.T
    S=A.T

    Parameters
    ----------
    Y : numpy.2darray
        Data matrix (n x d)

    irows : 1d-array
        The kappas rows of Y to be used for archetypes creation

    diag_less : float
       The expected mean distance from 1 for the diagonal elements of submatrix A[irows,:]

    verbose : bool
        Set True if running details should be printed

    Output
    ------
    BY : numpy.2darray
        (kappas x d) matrix

    A : numpy.2darray
        n x kappas matrix, row stochastic

    B : numpy.2darray
        kappas x n matrix, column stochastic

    irows : list
       The rows of data points that were used as archetypes in Python numbering

    SSE : float
        Sum of Squared Errors

    varexlp : float
        Percent variation explained by the model

    fin_iters : int
        The final number of iterations that was done

    time_elapsed : float
      The total elapsed time in seconds

    diagsum_final: float
        The sum of diagonal elements for the sub-matrix A[irows,:] that corresponds to archetypes

    """
    # Proceed to "py_pcha" entities:

    X = Y.T
    if verbose:
        print('Fast Archetypal Analysis:')
        print('Compute the compositions when the archetypes are already given')
        print()

    def s_update2(S, XCtX, CtXtXC, muS, SST, SSE, verbose=False, diag_less =diag_less):
        """Update S for one iteration of the algorithm."""
        kappas, J = S.shape
        e = np.ones((kappas, 1))
        fin_iters=0

        cond = True
        while cond:
            SSE_old = SSE
            g = (np.dot(CtXtXC, S) - XCtX) / (SST / J)
            g = g - e * np.sum(g.A * S.A, axis=0)
            S_old = S
            while True:
                fin_iters = fin_iters + 1
                S = (S_old - g * muS).clip(min=0)
                S = S / np.dot(e, np.sum(S, axis=0))
                SSt = S * S.T
                SSE = SST - 2 * np.sum(XCtX.A * S.A) + np.sum(CtXtXC.A * SSt.A)
                if verbose:
                    print('|%7.0f | %12.6e | %12.6e | %24.6f|' % (fin_iters, SSE_old, SSE, abs(SSE_old - SSE) / SSE))
                if SSE <= SSE_old * (1 + 1e-9):
                    muS = muS * 1.2
                    # cond1 = False
                    break
                else:
                    muS = muS / 2
            A=S.T
            diagsum = sum(np.diag(S.T[irows,]))
            cond = (diagsum < kappas - diag_less*kappas)

        return S, SSE, muS, fin_iters

    t1 = dt.now()
    # Parameters
    N, M = X.shape
    kappas = len(irows)
    SST = np.sum(X * X)
    i = irows
    j = range(kappas)
    # Create the matrix C which defines the archetypes
    C = csr_matrix((np.ones(len(i)), (i, j)), shape=(M, kappas)).todense()
    # Create the archetypes
    XC = np.dot(X, C)
    BY = XC.T
    # Parameters for S update
    muS = 1
    # Initialise S
    XCtX = np.dot(XC.T, X)
    CtXtXC = np.dot(XC.T, XC)
    S = -np.log(np.random.random((kappas, M)))
    S = S / np.dot(np.ones((kappas, 1)), np.mat(np.sum(S, axis=0)))
    SSt = np.dot(S, S.T)
    SSE = SST - 2 * np.sum(XCtX.A * S.A) + np.sum(CtXtXC.A * SSt.A)
    SSE_0 = SSE
    # S updates
    dheader1 = "| %6s | %12s | %12s | %15s |" % ("Iter", "SSE_i", "SSE_(i+1)", "|SSE_(i+1)-SSE_i|/SSE_i")
    dline1 = "|--------|--------------|--------------|-------------------------|"

    if verbose:
        print(dline1)
        print(dheader1)
        print(dline1)

    S, SSE, muS, fin_iters = s_update2(S, XCtX, CtXtXC, muS, SST, SSE, verbose=verbose, diag_less = diag_less)

    if verbose:
        print(dline1)
    varexpl = (SST - SSE) / SST
    #
    ss01 = "SSE_" + str(fin_iters) + " / SSE_0   "
    vss01 = SSE / SSE_0
    #
    t2 = dt.now()
    # (t2 - t1).seconds
    # (t2 - t1).microseconds
    # (t2 - t1).microseconds/1000
    time_elapsed = (t2 - t1).seconds
    if verbose:
        print('Time for the ' + str(fin_iters) + ' A updates was ' + str(time_elapsed) + ' secs')
        print()
        dheader2 = '|%9s | %10s | %12s | %10s | %12s |' % ('Iter', 'VarExpl', 'SSE', ss01, ' muA  ')
        dline2 = '|----------|------------|--------------|-------------------|--------------|'
        print(dline2)
        print(dheader2)
        print(dline2)
        print('|%9.0f | %10.6f | %10.6e | %17.6f | %13.4e|' % (fin_iters, varexpl, SSE, vss01, muS))
        print(dline2)
    # Return final results and indices
    BY = XC.T
    B = C.T
    A = S.T
    diagsum_final=sum(np.diag(A[irows,]))
    return BY, A, B, irows, SSE, varexpl, fin_iters, time_elapsed, diagsum_final

#
#######################
#

def grid_archetypal(df, diag_less = 1e-2, verbose = False):
    """Performs Grid Archetypal Analysis.
    For the data matrix Y (n x d):
    The Grid Archetypes are the expand grid of the [min,max] intervals of
    all available variables (columns) of df
    The number of Grid Archetypes is always:
          kappas = 2^d
    with d being the dimension  of the vector space formed by the columns of df.
    Then the stochastic A (n x kappas) matrix is computed such that
                             Y ~ ABY
    under the common Euclidean matrix norm.
    For that purpose the code of package "py_pcha":
    https://github.com/ulfaslak/py_pcha
    is used, under next definitions:
    X=Y.T
    C=B.T
    S=A.T

    Input
    ----------
    df : numpy.2darray
        Data matrix (n x d)

    diag_less : float
       The expected mean distance from 1 for the diagonal elements of submatrix A[irows,:]

    verbose : bool
        Set True if running details should be printed

    Output
    ------
    BY : numpy.2darray
        (kappas x d) matrix

    A : numpy.2darray
        (kappas + n) x kappas matrix, row stochastic for merged data

    B : numpy.2darray
        kappas x n matrix, column stochastic

    AM : numpy.2darray
        n x kappas data frame, row stochastic for initial data

    AMDF : pandas.DataFrame
        n x kappas data frame, row stochastic for initial data

    SSE : float
        Sum of Squared Errors

    varexlp : float
        Percent variation explained by the model

    fin_iters : int
        The final number of iterations that were done

    time_elapsed : float
        The total elapsed time in seconds

    diagsum_final: float
        The sum of diagonal elements for the sub-matrix A[irows,:] that corresponds to archetypes

    """
    TIME_1 = dt.now()
    # Create Grid
    minmax = [[np.min(df[:, i]), np.max(df[:, i])] for i in range(0, df.shape[1])]
    m2 = list(itertools.product(*minmax))
    BY = np.array(m2)
    kappas = BY.shape[0]
    # d1 = list([BY, df])
    # Merge Grid with Data
    dg = np.concatenate((BY, df), axis=0)
    # Run fast_archetypal for the merged datta with given archetypes the grid:
    # Rows are the first kappas ones:
    BY, A, B, irows, SSE, varexpl, fin_iters, time_elapsed, diagsum_final = fast_archetypal(dg,irows=range(BY.shape[0]), diag_less=diag_less, verbose=verbose)
    # diagsum = sum(np.diag(A))
    # Print the sum of diagonal elements that should be all ones:
    if verbose:
        print()
        print("The sum of diagonal elements for the sub-matrix of closer grid points is "+str(round(diagsum_final,3)))
        print("The ideal sum would be " + str(kappas))
        print()
    # Create the A matrix of compositions for the data points now:
    a_range = range(kappas, A.shape[0])
    AM = A[a_range, :]
    # Make a data frame too for it:
    AMDF = pd.DataFrame(AM)
    TIME_2 = dt.now()
    time_elapsed = (TIME_2 - TIME_1).seconds
    # Return
    return BY, A, B, AM, AMDF, SSE, varexpl, fin_iters, time_elapsed, diagsum_final


#
#######################
#

def closer_grid_archetypal(df, diag_less = 1e-2, verbose = False):
    """ Performs Grid Archetypal Analysis.
    For the data matrix Y (n x d):
    The Grid Archetypes are the expand grid of the [min,max] intervals of
    all available variables (columns) of df
    The number of Grid Archetypes is always:
          kappas = 2^d
    with d being the dimension  of the vector space formed by the columns of df.
    Next step is to find the closer data points to the Grid Archetypes
    and those are the matrix BY.
    Then the stochastic A (n x kappas) matrix is computed such that
                             Y ~ ABY
    under the common Euclidean matrix norm.
    For that purpose the code of package "py_pcha":
    https://github.com/ulfaslak/py_pcha
    is used, under next definitions:
    X=Y.T
    C=B.T
    S=A.T

    Input
    ----------
    df : numpy.2darray
        Data matrix (n x d)

    diag_less : float
       The expected mean distance from 1 for the diagonal elements of submatrix A[irows,:]

    verbose : bool
        Set True if running details should be printed

    Output
    ------
    BY : numpy.2darray
        (kappas x d) matrix

    A : numpy.2darray
        n x kappas matrix, row stochastic

    B : numpy.2darray
        kappas x n matrix, column stochastic

    ADF : pandas.DataFrame
        n x kappas data frame, row stochastic

    SSE : float
        Sum of Squared Errors

    imins : list
        The list of the rows that correspond to the closer to the Grid Archetypes points
        in the Python terminology - begins from zero

    varexlp : float
       Percent variation explained by the model

    fin_iters : int
        The final number of iterations that were done

    time_elapsed : float
        The total elapsed time in seconds

    diagsum_final: float
        The sum of diagonal elements for the sub-matrix A[irows,:] that corresponds to archetypes

    """
    TIME_1=dt.now()
    # Find the Grid Archetypes:
    minmax = [[np.min(df[:, i]), np.max(df[:, i])] for i in range(0, df.shape[1])]
    m2 = list(itertools.product(*minmax))
    GA = np.array(m2)
    # Store the number of archetypes
    kappas = GA.shape[0]
    # Find the Closer to Grid Archetypes:
    # https://jaykmody.com/blog/distance-matrices-with-numpy/
    Y1 = df
    Y2 = GA
    x2 = np.sum(Y1 ** 2, axis=1)
    y2 = np.sum(Y2 ** 2, axis=1)
    xy = np.matmul(Y1, Y2.T)
    x2 = x2.reshape(-1, 1)
    dists = np.sqrt(x2 - 2 * xy + y2)
    # Find minimum distance points
    imins = [np.argmin(dists[:, i]) for i in range(0, dists.shape[1])]
    # Run fast_archetypal for the merged datta with given archetypes the closer to the grid ones:
    BY, A, B, irows, SSE, varexpl, fin_iters, time_elapsed, diagsum_final = fast_archetypal(df, irows=imins, diag_less=diag_less, verbose=verbose)
    # Find the sub matrix with closer to grid points and check the ones:
    if verbose:
        print()
        print("The sum of diagonal elements for the sub-matrix of closer grid points is "+str(round(diagsum_final,3)))
        print("The ideal sum would be " + str(kappas))
        print()
    # Return the A matrix for data points as a data frame too
    ADF = pd.DataFrame(A)
    TIME_2 = dt.now()
    time_elapsed = (TIME_2-TIME_1).seconds
    # Return
    return BY, A, B, ADF, imins, SSE, varexpl, fin_iters, time_elapsed, diagsum_final

#
#######################
#
