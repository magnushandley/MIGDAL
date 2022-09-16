% Alex Mills  24.June.2021

% Returns a 2D, square, centered Gaussian filter.
% The Gaussian is normalized so that the peak has an amplitude of 1.

% n is the side length of the square.
% sigma is the width of the Gaussian.


function [gauss] = Gaussian2d(n,sigma)

sweep = sigma*n/2;

kernel = round(sweep/sigma);
index = 1:n;
matrix = ones(n);
matrix = matrix(:,1).*index;

ogauss = (1/((4*pi)^0.5*sigma)).*exp(-((matrix - kernel - 1).^2 +...
    (matrix' - kernel - 1).^2)./(2*sigma^2));

gauss = ogauss./max(ogauss(:));

end