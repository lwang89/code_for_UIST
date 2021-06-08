function [dO_I, dD_I, dO_phi, dD_phi] = preprocess(SSY0_I, SSY0_phi, A_I, A_phi, B_I, B_phi, t)


    rho=[25, 35]; %mm
    lambda=[830, 690];

    % Example data from (Subject 4):
    %   Blaney, G, Sassaroli, A, Pham, T, Fernandez, C, Fantini, S. Phase
    %   dual?slopes in frequency?domain near?infrared spectroscopy for enhanced
    %   sensitivity to brain tissue: First applications to human subjects. J.
    %   Biophotonics. 2019;e201960018. https://doi.org/10.1002/jbio.201960018

    % Physical locations: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    %                     ~   Src1     DetA   DetB     Src2   ~
    %                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    % Data format: Det_Y(time, srcInd)
    % Confirm: ?????src??????????
    %              | srcInd | location | wavelength |
    %              |      1 |     Src1 |          1 690|
    %              |      2 |     Src2 |          1 690|
    %              |      3 |     Src1 |          2 830|
    %              |      4 |     Src2 |          2 830|

    % Parsed format: Y(time, pair, wavelength)
    %                Where "Y" is the datatype (I or phi)

    % Intensity ??????????????????????????????????????phase
    I(:, :, 1)=[A_I(:, 1), B_I(:, 1), B_I(:, 2), A_I(:, 2)]; %counts
    I(:, :, 2)=[A_I(:, 3), B_I(:, 3), B_I(:, 4), A_I(:, 4)]; %counts

    % Phase ??
    phi(:, :, 1)=[A_phi(:, 1), B_phi(:, 1), B_phi(:, 2), A_phi(:, 2)]...
        *pi/180; %rad
    phi(:, :, 2)=[A_phi(:, 3), B_phi(:, 3), B_phi(:, 4), A_phi(:, 4)]...
        *pi/180; %rad


    %% Initialize Coefficients
    %% what are the meanings of these parameters?
    opts.rho=rho;
    opts.nin=1.333;
    % opts.fmod=140.625e6; %Hz
    opts.fmod=110e6;
    opts.mua=0.01; %1/mm
    opts.musp=1; %1/mm

    % ?????later?????
    [DSF_I, DSF_phi]=initDSF(opts);
    [Oext, Dext]=initExtCoe(lambda);


    coes_I.DSF=DSF_I;
    coes_I.Oext=Oext;
    coes_I.Dext=Dext;

    coes_phi=coes_I;
    coes_phi.DSF=DSF_phi;

    % i1: start point
    % i2: end point
    i1 = 1;
    i2 = length(t);
    inds = i1 : i2;

        
    [dO_I, dD_I]=DS2OandD(I(inds, :, :),...
        SSY0_I, 'intensity', rho, coes_I);
    [dO_phi, dD_phi]=DS2OandD(phi(inds, :, :),...
        SSY0_phi, 'phase', rho, coes_phi);

end