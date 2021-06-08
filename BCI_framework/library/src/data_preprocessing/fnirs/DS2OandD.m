function [dO, dD] = DS2OandD(Y, SSY0, dataTyp, rho, coes)
% [dO, dD] = DS2OandD(Y, SSY0, dataTyp, rho, coes)
%   Giles Blaney (Giles.Blaney@tufts.edu) Fall 2019
%   
%   Blaney, G, Sassaroli, A, Pham, T, Fernandez, C, Fantini, S. Phase
%   dual?slopes in frequency?domain near?infrared spectroscopy for enhanced
%   sensitivity to brain tissue: First applications to human subjects. J.
%   Biophotonics. 2019;e201960018. https://doi.org/10.1002/jbio.201960018
%   
%   Inputs:
%       Y           - Time X 4 X wavelength matrix of intensity or phase 
%                     data with following columns: 
%                     Y(tn, :, wn)=[Short1, Long1, Short2, Long2].
%       SSY0        - 1 X pair X wavelength matrix of baseline intensity or
%                     phase slopes.
%       dataTyp     - String specifying datatype, either 'intensity' or
%                     'phase'. If datatype is 'phase' the units of Y are 
%                     rad.
%       rho         - Array of source detector distances in mm.
%       coes        - Coefficients structure containing the following 
%                     fields:
%                     ~ DSF    - Differential slope factor.
%                     ~ Oext   - Oxyhemoglobin extinction coefficient in 
%                                1/(uM mm).
%                     ~ Dext   - Deoxyhemoglobin extinction coefficient in 
%                                1/(uM mm).
%   Outputs:
%       dO          - Oxyhemoglobin concentration changes in uM.
%       dD          - Deoxyhemoglobin concentration changes in uM.
    
    %% Parse Input
    if nargin<=2
        dataTyp='intensity';
        warning('Assuming intensity data');
    end
    if nargin<=3
        rho=[25, 35]; %mm
        warning('Assuming default geometry');
    end
    
    if nargin<=1
        SSY0=DScalcSSY0(Y, dataTyp, rho);
        warning('Assuming default baseline');
    end
    
    if nargin<=4
        [DSF_I, DSF_phi]=initDSF;
        switch dataTyp
            case 'intensity'
                DSF=DSF_I;
            case 'phase'
                DSF=DSF_phi;
            otherwise
                error('Choose either intensity or phase datatype');
        end
        
        lambda=[830, 690]; %nm
        [Oext, Dext]=initExtCoe(lambda);
        extMat=[Oext.', Dext.'];
        
        warning('Assuming default coefficients and wavelengths');
    else
        DSF=coes.DSF;
        extMat=[coes.Oext.', coes.Dext.'];
    end
    
    %% Extract Dual-Slope (DS)
    dmua=NaN(size(Y, 1), size(Y, 3));
    for lInd=1:size(Y, 3)
        switch dataTyp
            case 'intensity'
                SS(:, 1)=(log(rho(2)^2*Y(:, 2, lInd))-...
                    log(rho(1)^2*Y(:, 1, lInd)))/diff(rho);
                SS(:, 2)=(log(rho(2)^2*Y(:, 4, lInd))-...
                    log(rho(1)^2*Y(:, 3, lInd)))/diff(rho);
            case 'phase'
                SS(:, 1)=wrapToPi(Y(:, 2, lInd)-Y(:, 1, lInd))/...
                    diff(rho);
                SS(:, 2)=wrapToPi(Y(:, 4, lInd)-Y(:, 3, lInd))/...
                    diff(rho);
            otherwise
                error('Choose either intensity or phase datatype');
        end

        dSS=SS-SSY0(:, :, lInd);
        dDS=(dSS(:, 1)+dSS(:, 2))/2;

        %% Convert to Absorption Changes (dmua)
        dmua(:, lInd)=-dDS/DSF;
    end
    
    %% Convert to Consentration Changes 
    X=linsolve(extMat, dmua.');
    dO=X(1, :).'; %uM
    dD=X(2, :).'; %uM
    
end