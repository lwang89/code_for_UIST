function [Oext, Dext] = initExtCoe(lambda)
% [Oext, Dext] = initExtCoe(lambda)
%   Giles Blaney (Giles.Blaney@tufts.edu) Fall 2019
%   
%   Bigio, I., & Fantini, S. (2016). Quantitative Biomedical Optics:
%   Theory, Methods, and Applications (Cambridge Texts in Biomedical
%   Engineering). Cambridge: Cambridge University Press.
%   doi:10.1017/CBO9781139029797
%   
%   Inputs:
%       lambda  - 1 X wavelengths vector of wavelengths in nm.
%   Outputs:
%       Oext    - Oxyhemoglobin extinction coefficient in 1/(uM mm).
%       Dext    - Deoxyhemoglobin extinction coefficient in 1/(uM mm).

    
    %% Parse Input
    if size(lambda, 1)~=1
        lambda=lambda.';
    end
    
    %% Interpolate Extinction Spectra
    spectra=load('OandDspect.mat');
    Oext=interp1(spectra.lambda, spectra.Oext, lambda); %1/(mM cm)
    Dext=interp1(spectra.lambda, spectra.Dext, lambda); %1/(mM cm)
    Oext=Oext/(1000*10); %1/(uM mm)
    Dext=Dext/(1000*10); %1/(uM mm)
    
end

