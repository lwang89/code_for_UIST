function [DSF_I, DSF_phi] = initDSF(opts)
% [DSF_I, DSF_phi] = initDSF(opts)
%   Giles Blaney (Giles.Blaney@tufts.edu) Fall 2019
%   
%   Blaney, G, Sassaroli, A, Pham, T, Fernandez, C, Fantini, S. Phase
%   dual?slopes in frequency?domain near?infrared spectroscopy for enhanced
%   sensitivity to brain tissue: First applications to human subjects. J.
%   Biophotonics. 2019;e201960018. https://doi.org/10.1002/jbio.201960018
%   
%   Inputs:
%       opts        - Options structure containing the following fields:
%                     ~ rho    - Array of source detector distances in mm.
%                     ~ nin    - Assumed index of refection inside the 
%                                medium, note it is assumed the outside 
%                                index of refraction is 1.
%                     ~ fmod   - Frequency domain modulation frequency in 
%                                Hz.
%                     ~ mua    - Assumed baseline absorption coefficient 
%                                within the medium in 1/mm.
%                     ~ musp   - Assumed baseline reduced scattering
%                                coefficient within the medium in 1/mm.
%   Outputs:
%       DSF_I       - Differential slope factor for intensity.
%       DSF_phi     - Differential slope factor for phase.
    
    %% Parse Input
    %% nargin:number of inputs, ????
    if nargin<=0
        opts.rho=[25, 35]; %mm
        opts.nin=1.333;
        opts.fmod=140.625e6; %Hz
        opts.mua=0.01; %1/mm
        opts.musp=1; %1/mm
        warning('Assuming default properties and geometry');
    end
    
    %% Calculate Differential Slope Factor (DSF)
    optProp.nin=opts.nin;
    optProp.nout=1;
    optProp.mua=opts.mua;
    optProp.musp=opts.musp;
    fmod=opts.fmod;
    rho=opts.rho;
    
    rhoAvg=mean(rho);
    rhoDel=diff(rho);
    rho1=rhoAvg-rhoDel/2;
    rho2=rhoAvg+rhoDel/2;
    den=rho1^2+rho2^2-2*rho1*rho2;
    
    [L1, ~]=complexTotPathLen(...
        [1/optProp.musp, 0, 0], [0, rho1, 0], 2*pi*fmod, optProp);
    [L2, ~]=complexTotPathLen(...
        [1/optProp.musp, 0, 0], [0, rho2, 0], 2*pi*fmod, optProp);
    
    dL_I=real(L2)-real(L1);
    dL_phi=imag(L2)-imag(L1);
    
    DSF_I=rhoDel*dL_I/den;
    DSF_phi=rhoDel*dL_phi/den;
    
end

%% Functions
function [L, R] = complexTotPathLen(rs, rd, omega, optProp)
% Giles Blaney Spring 2019
% [L, R] = complexTotPathLen(rs, rd, omega, optProp)
% Inputs:
%   rs      - Source corrdinates. (mm)
%   rd      - Detector corrdinates. (mm)
%   omega   - (OPTIONAL, default=2*pi*1.40625e8 rad/sec) Angular modulation
%             frequecy. (rad/sec)
%   optProp - (OPTIONAL) Struct of optical properties with the following
%             fields:
%                nin  - (default=1.4) Index of refraction inside. (-)
%                nout - (default=1) Index of refraction outside. (-)
%                musp - (default=1.2 1/mm) Reduced scattering. (1/mm)
%                mua  - (default=0.01 1/mm) Absorption. (1/mm)
% Outputs:
%   L       - Complex total pathlength. (mm)
%   R       - Complex reflectance. (1/mm^2)

    if nargin<=2
        fmod=1.40625e8; %Hz
        omega=2*pi*fmod; %rad/sec
        
        optProp.nin=1.4;
        optProp.nout=1;
        optProp.musp=1.2; %1/mm
        optProp.mua=0.01; %1/mm
        
        warning(['Default optical properties used, this may be inconsistent'...
            ' with the musp used for source depth']);
    end

    if size(rs, 1)>1 && size(rd, 1)>1
        error('Can not use multiple sources and multiple detectors');
    end
    
    x0=rs(:, 1); %mm
    y0=rs(:, 2); %mm
    z0=rs(:, 3); %mm

    c=2.99792458e11; %mm/sec
    v=c/optProp.nin;

    A=n2A(optProp.nin, optProp.nout);
    D=1/(3*optProp.musp); %mm
    xb=-2*A*D; %mm

    mueff=sqrt(optProp.mua/D-1i*omega/(v*D)); %1/mm

    rsp=[-x0+2*xb, y0, z0]; %mm

    r1=vecnorm(rd-rs, 2, 2);
    r2=vecnorm(rd-rsp, 2, 2);
    
    R=complexReflectance(rs, rd, omega, optProp);
    L=((x0./r1).*exp(-mueff.*r1)+((x0-2.*xb)./r2).*exp(-mueff.*r2))./...
        (8*pi*D*R);
end

function [R] = complexReflectance(rs, rd, omega, optProp)
% Giles Blaney Spring 2019
% [R] = complexReflectance(rs, rd, omega, optProp)
% Inputs:
%   rs      - Source corrdinates. (mm)
%   rd      - Detector corrdinates. (mm)
%   omega   - (OPTIONAL, default=2*pi*1.40625e8 rad/sec) Angular modulation
%             frequecy. (rad/sec)
%   optProp - (OPTIONAL) Struct of optical properties with the following
%             fields:
%                nin  - (default=1.4) Index of refraction inside. (-)
%                nout - (default=1) Index of refraction outside. (-)
%                musp - (default=1.2 1/mm) Reduced scattering. (1/mm)
%                mua  - (default=0.01 1/mm) Absorption. (1/mm)
% Outputs:
%   R       - Complex reflectance. (1/mm^2)

    if nargin<=2
        fmod=1.40625e8; %Hz
        omega=2*pi*fmod; %rad/sec
        
        optProp.nin=1.4;
        optProp.nout=1;
        optProp.musp=1.2; %1/mm
        optProp.mua=0.01; %1/mm
        
        warning(['Default optical properties used, this may be inconsistent'...
            ' with the musp used for source depth']);
    end

    if size(rs, 1)>1 && size(rd, 1)>1
        error('Can not use multiple sources and multiple detectors');
    end
    
    x0=rs(:, 1); %mm
    y0=rs(:, 2); %mm
    z0=rs(:, 3); %mm

    c=2.99792458e11; %mm/sec
    v=c/optProp.nin;

    A=n2A(optProp.nin, optProp.nout);
    D=1/(3*optProp.musp); %mm
    xb=-2*A*D; %mm

    mueff=sqrt(optProp.mua/D-1i*omega/(v*D)); %1/mm

    rsp=[-x0+2*xb, y0, z0]; %mm

    r1=vecnorm(rd-rs, 2, 2);
    r2=vecnorm(rd-rsp, 2, 2);
    
    R=(x0.*(1./r1+mueff).*exp(-mueff.*r1)./(r1.^2)+...
        (x0-2*xb).*(1./r2+mueff).*exp(-mueff.*r2)./(r2.^2))/...
        (4*pi);
end

function A = n2A(nin, nout)

    if nargin==0
        dan12=1.4;
    else
        dan12=nin/nout;
    end

    if dan12>1
        A=504.332889-2641.00214*dan12+...
            5923.699064*dan12.^2-7376.355814*dan12^3+...
            5507.53041*dan12^4-2463.357945*dan12^5+...
            610.956547*dan12^6-64.8047*dan12^7;
    elseif dan12<1
        A=3.084635-6.531194*dan12+...
            8.357854*dan12^2-5.082751*dan12^3+1.171382*dan12^4;
    else
        A=1;
    end

end