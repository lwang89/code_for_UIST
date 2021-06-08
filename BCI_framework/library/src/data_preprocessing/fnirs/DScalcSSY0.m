function SSY0 = DScalcSSY0(Y0, dataTyp, rho)
% SSY0 = DScalcSSY0(Y0, dataTyp, rho)
%   Giles Blaney (Giles.Blaney@tufts.edu) Fall 2019
%   
%   Blaney, G, Sassaroli, A, Pham, T, Fernandez, C, Fantini, S. Phase
%   dual?slopes in frequency?domain near?infrared spectroscopy for enhanced
%   sensitivity to brain tissue: First applications to human subjects. J.
%   Biophotonics. 2019;e201960018. https://doi.org/10.1002/jbio.201960018
%   
%   Inputs:
%       Y0          - Time X 4 X wavelength of intensity or phase basleine
%                     data with following columns: 
%                     Y0=[Short1, Long1, Short2, Long2].
%       dataTyp     - String specifying datatype, either 'intensity' or
%                     'phase'. If datatype is 'phase' the units of Y0 are 
%                     rad.
%       rho         - Array of source detector distances in mm.
%   Outputs:
%       SSY0        - 1 X pair X wavelength matrix of baseline intensity or
%                     phase slopes.
    
    %% Parse Input
    if nargin<=1
        dataTyp='intensity';
        warning('Assuming intensity data');
    end
    if nargin<=2
        rho=[25, 35]; %mm
        warning('Assuming default geometry');
    end
    
    %% Extract Dual-Slope (DS)
    SSY0=NaN(1, 2, size(Y0, 3));
    switch dataTyp
        case 'intensity'
            for lInd=1:size(Y0, 3)
                SSY0(1, 1, lInd)=mean((log(rho(2)^2*Y0(:, 2, lInd))-...
                    log(rho(1)^2*Y0(:, 1, lInd)))/diff(rho));
                SSY0(1, 2, lInd)=mean((log(rho(2)^2*Y0(:, 4, lInd))-...
                    log(rho(1)^2*Y0(:, 3, lInd)))/diff(rho));
            end
        case 'phase'
            for lInd=1:size(Y0, 3)
                SSY0(1, 1, lInd)=mean(wrapToPi(Y0(:, 2, lInd)-...
                    Y0(:, 1, lInd))/diff(rho));
                SSY0(1, 2, lInd)=mean(wrapToPi(Y0(:, 4, lInd)-...
                    Y0(:, 3, lInd))/diff(rho));
            end
        otherwise
            error('Choose either intensity or phase datatype');
    end
    
end