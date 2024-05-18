#TIMEIT=0; # 1 to enable time printing at some stages
tmp=try(flush(fclog), silent=TRUE)
if (length(find("TIMEIT")) && TIMEIT && !inherits(tmp, "try-error")) {
   cat("load    : ", format(Sys.time()), " cpu=", proc.time()[1L], "\n", sep="", file=fclog)
}
build_mult_bxxc=function(dirx) {
   fcpp="mult_bxxc.cpp"
   fso=paste("mult_bxxc", .Platform$dynlib.ext, sep="")
   if (!file.exists(file.path(dirr, "mult_bxxc.txt")) || !file.exists(file.path(dirr, fso)) ||
      file.mtime(file.path(dirr, fso)) < file.mtime(file.path(dirr, fcpp))) {
      # freshly compile the code (==first use or .so is outdated)
      frmu=file.path(system.file(package="rmumps"), "libs", .Platform$r_arch, paste("rmumps", .Platform$dynlib.ext, sep=""))
      Sys.setenv(PKG_LIBS=sprintf('"%s"', frmu))
      Sys.setenv(PKG_CXXFLAGS="-std=c++11 -fopenmp") # ‑mveclibabi=svml
      tes=capture.output(sourceCpp(file.path(dirr, "mult_bxxc.cpp"), verbose=TRUE))
      dl_str=grep("dyn.load", tes, value=TRUE)
      ftmp=sub(".*'(.*)'.*", "\\1", dl_str)
      dl_inf=sub("^(.*) <- dyn.load\\(.*$", "\\1", dl_str)
      fu_li=sub("// ", "", grep("// ", tes, value=TRUE))
      file.copy(ftmp, file.path(dirr, fso), overwrite = TRUE, copy.date=TRUE)
      sy=sapply(fu_li, function(it) {s=grep(paste(it, " <- ", sep=""), tes, value=TRUE, fixed=TRUE); sub(dl_inf, "multdll", s)})
      write.table(sy, file=file.path(dirr, "mult_bxxc.txt"), col.names=FALSE, row.names=FALSE)
   }
}
# build compiled code
#build_mult_bxxc(dirx)
#browser()
so=.Platform$dynlib.ext
#fso=paste("mult_bxxc", so, sep="")
## define R functions from mult_bxxc.so
#multdll=dyn.load(file.path(dirr, fso))
#sy=as.matrix(read.table(file=file.path(dirr, "mult_bxxc.txt"), header=FALSE))[,1L]
#for (rsy in sy) {
#   eval(parse(text=rsy))
#}
#rm(multdll)

dfcg2fallnx=function(nbl, flnx, param, fc, fg) {
   # produce complete flux (net,xch)*(dep,free,constr,growth) vector
   # from dep,free,constr,growth
   f=c(flnx[seq_len(nbl$fln)], param[seq_len(nbl$ffn)], fc[seq_len(nbl$fcn)], fg,
      flnx[nbl$fln+seq_len(nbl$flx)], param[nbl$ffn+seq_len(nbl$ffx)], fc[nbl$fcn+seq_len(nbl$fcx)], numeric(nbl$fgr))
   return(f)
}

cumo_resid=function(param, cjac=TRUE, labargs) {
   nmlocal=c("jx_f", "pool", "measurements", "nml", "ir2isc", "jacobian", "nbl", "nbexp", "noscale")
   for (item in nmlocal) {
      assign(item, labargs[[item]])
   }
   # find x for all weights and experiments
   lres=lab_sim(param, cjac, labargs)
   if (!is.null(lres$err) && lres$err)
      return(list(err=1L, mes=lres$mes))

   # find simulated normalized measurement vector v=(measmat*x); v/sum(v) where appropriate
   if (is.null(jx_f$simlab))
      jx_f$simlab=jx_f$ureslab=jx_f$reslab=setNames(vector("list", nbl$exp), nml$exp)

   if (!noscale && is.null(labargs$sfi))
      labargs$sfi=lapply(nbl$sc, double) # place for inverse sums for scaling factors
   for (iexp in seq_len(nbl$exp)) {
      jx_f$simlab[[iexp]]=jx_f$usimlab[[iexp]]
      if (!noscale && nbl$sc[[iexp]] > 0L) {
         isc=1L;
         for (ir in sc[[iexp]]) {
            s=1./sum(jx_f$simlab[[iexp]][ir])
            labargs$sfi[[iexp]][isc]=s
            bop(jx_f$simlab[[iexp]], as.matrix(ir), "*=", s)
            isc=isc+1L
         }
      }
      names(jx_f$simlab[[iexp]])=names(jx_f$usimlab[[iexp]])=names(measurements$vec$labeled[[iexp]])
      # diff between simulated and measured
      jx_f$ureslab[[iexp]]=(jx_f$simlab[[iexp]]-measurements$vec$labeled[[iexp]])
      jx_f$reslab[[iexp]]=jx_f$ureslab[[iexp]]/measurements$dev$labeled[[iexp]]
   }

   # diff between simulated and measured
   pool[nml$poolf]=param[nml$poolf]
   jx_f$simfmn=jx_f$lf$fallnx[nml$fmn]
   jx_f$simpool=(measurements$mat$pool %stm% pool)[,1L]
   jx_f$uresflu=jx_f$simfmn-measurements$vec$flux
   jx_f$resflu=jx_f$uresflu/measurements$dev$flux
   jx_f$urespool=jx_f$simpool-measurements$vec$pool
   jx_f$respool=jx_f$urespool/measurements$dev$pool
   jx_f$res=c(unlist(jx_f$reslab), jx_f$resflu, jx_f$respool)
   jx_f$res[measurements$outlier]=NA
   jx_f$ures=c(unlist(jx_f$ureslab), jx_f$uresflu, jx_f$urespool)

   if (cjac) {
#browser()
      # jacobian
      cumo_jacob(param, labargs)
      if (is.null(labargs$jacobian))
         labargs$jacobian=structure(matrix(0., nbl$resid, nbl$param), dimnames=list(nml$resid, nml$param))
#require(numDeriv)
#r=function(p) cumo_resid(p, F, labargs)$res
#jacobian=jacobian(r, param)
      bop(labargs$jacobian, 1L, "=", jx_f$udr_dp*measurements$dev$all_inv)
      jx_f$jacobian=labargs$jacobian
      jx_f$dr_dff=jx_f$jacobian[,seq_len(nbl$ff),drop=FALSE]
      return(list(res=jx_f$res, jacobian=jx_f$jacobian))
   } else {
      return(list(res=jx_f$res))
   }
}

cumo_cost=function(param, labargs, resl=lab_resid(param, cjac=FALSE, labargs)) {
   if (!is.null(resl$err) && resl$err) {
      return(NA)
   }
   res=resl$res
   if (is.null(res))
      return(NA)
   iva=!is.na(res)
   vres=res[iva]
   fn=crossprod(vres)[1L]
   return(fn)
}

param2fl=function(param, labargs) {
   # claculate all fluxes from free fluxes
   
   # local variabl assignments from labargs
   nmlocal=c("nbl", "nml", "invAfl", "pcgc2bfl", "bp", "g2bfl", "fc")
   for (item in nmlocal) {
      assign(item, labargs[[item]])
   }
   
   fg=numeric(nbl$fgr)
   names(fg)=nml$fgr
   if (nbl$fgr > 0L) {
      fg[paste("g.n.", substring(nml$poolf, 4L), "_gr", sep="")]=nbl$mu*param[nml$poolf]
   }
   flnx=setNames(as.numeric(invAfl%*%(pcgc2bfl %stm% c(param[seq_len(nbl$ff)], fc, fg, 1.))), nml$fl)
   fallnx=setNames(c(dfcg2fallnx(nbl, flnx, param, fc, fg)), nml$fallnx)
   fwrv=setNames(c(fallnx2fwrv(fallnx, nbl)), nml$fwrv)
   lf=list(fallnx=fallnx, fwrv=fwrv, flnx=flnx)
   labargs$jx_f$lf=lf
   return(lf)
}

param2fl_x=function(param, cjac=TRUE, labargs, fullsys=FALSE) {
   # translate free params (fluxes+scales) to fluxes and cumomers
   # or emus
   # local variabl assignments form labargs
   nmlocal=ls(labargs)
   for (item in nmlocal) {
      assign(item, labargs[[item]])
   }
   if (fullsys) {
      nbx=nbl$xf
      nbxi=nbl$xif
      xi=xif
      nmx=nml$cumo
      spa=spaf
      rcumo_in_cumo=match(nml$rcumo, nmx)
   } else {
      nbx=nbl$x
      nbxi=nbl$xi
      nmx=nml$x
      nbx=nbl$x
   }
   nbw=length(nbx)
   nbc_x=cumsum(c(0L, nbx))
   nbff=nbl$ff
   nbpoolf=nbl$poolf
   nbfgr=nbl$fgr
   nbmeas=nbl$meas
   nmexp=nml$exp
   nbexp=nbl$exp
   fg=nbl$mu*param[nml$poolf] # the same alphabetical order
   names(fg)=nml$fgr
   pool[nml$poolf]=param[nml$poolf] # inject variable pools to pool vector

   # calculate all fluxes from free fluxes
   lf=param2fl(param, labargs)
   if (is.null(jx_f$x) || nrow(jx_f$x) != sum(nbx)) {
      jx_f$x=matrix(0., nrow=sum(nbx), nbl$exp)
      dimnames(jx_f$x)=list(nmx, nmexp)
      jx_f$usimlab=vector("list", nbl$exp)
      names(jx_f$usimlab)=nmexp
   }
   x=jx_f$x
   usimlab=jx_f$usimlab
   if (is.null(labargs$incu) || length(labargs$incu) != 1L+nbxi+nbc_x[nbw+1L]) {
      labargs$incu=incu=lapply(seq_len(nbexp), function(iexp) c(1., xi[[iexp]], double(nbc_x[nbw+1L])))
      jx_f$dux_dp=lapply(seq_len(nbl$exp), function(iexp) matrix(0., nbmeas[[iexp]], nbff+nbpoolf))
   }
   Ali=lapply(seq_len(nbw), function(iw) fwrv2Abr(lf$fwrv, spa[[iw]], NULL, NULL, getb=FALSE, emu=emu)$A)
   if (cjac) {
      # derivation of fwrv fluxes by free parameters: free fluxes+concentrations
      mdf_dffp=df_dffp(param, jx_f$lf$flnx, nbl, nml)
      jx_f$df_dffp=mdf_dffp
      if (is.null(labargs$x_f))
         labargs$x_f=matrix(0., nrow=sum(nbx), ncol=nbff+nbfgr)
      x_f=labargs$x_f
      if (is.null(jx_f$x_f))
         jx_f$x_f=vector("list", nbl$exp)
   } else {
      x_f=NULL
   }
   for (iexp in seq_len(nbl$exp)) {
      if (length(ipwe[[iexp]])) {
         # prepare measurement pooling operations
         pwe[[iexp]][ipwe[[iexp]]]=pool[ip2ipwe[[iexp]]]
         spwe=tapply(pwe[[iexp]], pool_factor[[iexp]], sum)
         spwe=1./spwe[nml$measmat[[iexp]]]
         pwe[[iexp]]=c(pwe[[iexp]]*spwe)
      }
      # construct the system A*x=b from fluxes
      # and find x for every weight
      # if fj_rhs is not NULL, calculate jacobian x_f
      if (cjac) {
         if (length(ijpwef[[iexp]])) {
            dpwe=-pwe[[iexp]]*spwe
            # dpwe is shortened to non zero entries in dpw_dpf
            dpwe=ifelse(ipf_in_ppw[[iexp]][ijpwef[[iexp]][,1L]]==ijpwef[[iexp]][,2L], (spwe+dpwe)[ijpwef[[iexp]][,1L]], dpwe[ijpwef[[iexp]][,1L]])
         }
      }
      
      # simulate labeling weight by weight
      ba_x=0L
      for (iw in seq_len(nbw)) {
         nbc=spa[[iw]]$nbc
         emuw=ifelse(emu, iw, 1L)
         if (nbc == 0L)
            next
         ixw=nbc_x[iw]+seq_len(nbx[iw])
         incuw=(1L+nbxi)+ixw
         b=fwrv2Abr(lf$fwrv, spa[[iw]], incu[[iexp]], if (emu) nml$emu[[iexp]][ixw] else nmx[ixw], getA=FALSE, emu=emu)$b
         xw=try(solve(Ali[[iw]], b), silent=TRUE)
         if (inherits(xw, "try-error")) {
            rerr=attr(xw, "condition")
            if (length(grep("rmumps:.*info\\[1\\]=-10,", rerr$message, fixed=FALSE))) {
               # find 0 rows if any
               l=spa[[iw]]
               ag=aggregate(abs(lf$fwrv[l$ind_a[,"indf"]]), list(l$ind_a[,"ir0"]), sum)
               izc=ag$Group.1[ag$x <= 1.e-10]
               izf=names(which(abs(lf$fwrv)<1.e-7))
               mes=paste("Cumomer matrix is singular. Try '--clownr N' or/and '--zc N' options with small N, say 1.e-3\nor constrain some of the fluxes listed below to be non zero\n",
                  "Zero rows in cumomer matrix A at weight ", iw, ":\n",
                  paste(nml$x[ixw][izc+1], collapse="\n"), "\n",
                  "Zero fluxes are:\n",
                  paste(izf, collapse="\n"), "\n",
                  sep="")
            } else {
               mes=as.character(rerr$message)
            }
            return(list(x=NULL, iw=iw, fA=Ali[[iw]], err=1L, mes=mes))
         }
         if (emu)
            xw=c(xw, 1.-rowSums(xw))
         incu[[iexp]][incuw]=xw
         if (cjac && nbff+nbfgr > 0L) {
            # calculate jacobian x_f
            # first, calculate right hand side for jacobian calculation
            # j_rhsw, b_x from sparse matrices
            # bind cumomer vector
            j_b_x=fx2jr(jx_f$lf$fwrv, spa[[iw]], nbl, incu[[iexp]])
            j_rhsw=j_b_x$j_rhsw %stm% mdf_dffp
            b_x=j_b_x$b_x
            if (iw > 1L)
               if (ba_x > 0L)
                  bop(j_rhsw, 1L, "+=", b_x %stm% x_f[seq_len(ba_x),,drop=FALSE])
            redim(j_rhsw, c(nbc, emuw*(nbff+nbfgr)))
            tmp=try(solve(Ali[[iw]], j_rhsw))
            if (inherits(tmp, "try-error")) {
               #browser()
               mes="Some obscure problem with label matrix.\n"
               return(list(x=NULL, iw=iw, fA=Ali[[iw]], err=1L, mes=mes))
            } else {
               bop(j_rhsw, 1L, "=", tmp)
            }
            if (emu) {
               redim(j_rhsw, c(nbc, iw, nbff+nbfgr))
               bop(x_f, c(1L, ba_x, iw*nbc), "=", j_rhsw)
               # m+N component
               #x_f[ba_x+iw*nbc+seq_len(nbc),]= -apply(j_rhsw, c(1L,3L), sum)
               bop(x_f, c(1L, ba_x+iw*nbc, nbc), "=", -arrApply(j_rhsw, 2L, "sum"))
            } else {
               bop(x_f, c(1L, ba_x, nbc), "=", j_rhsw)
            }
         }
         ba_x=ba_x+nbx[iw]
      }
   
      #rownames(incu)=c("one", nml$inp, nml$x)
      x[, iexp]=tail(incu[[iexp]], -nbxi-1L)
      
      # calculate unreduced and unscaled measurements
      mx=(measmat[[iexp]] %stm% (if (nrow(x) == ncol(measmat[[iexp]]))
            x[, iexp] else
            x[rcumo_in_cumo, iexp]))[,1L]+memaone[[iexp]]
      # measurement vector before pool ponderation
      mv=if (length(ipwe[[iexp]])) meas2sum[[iexp]] %stm% (pwe[[iexp]]*mx) else mx
      jx_f$usimlab[[iexp]]=as.numeric(mv)
      if (cjac) {
         # free flux part of jacobian (and partially free pools if present in x_f)
         if (nbff+nbfgr > 0L) {
            mffg=measmat[[iexp]] %stm% x_f
            if (length(ipwe[[iexp]])) {
               mffg=meas2sum[[iexp]] %stm% (pwe[[iexp]]*mffg)
            }
         } else {
            mffg=matrix(0., nrow=nbmeas[[iexp]], ncol=0L)
         }
         # free pool part of jacobian
         mff=mffg
         mpf=matrix(0., nrow=nbmeas[[iexp]], ncol=nbl$poolf)
         if (length(ijpwef[[iexp]]) > 0L) {
            # derivation of pool weights
            dpw_dpf[[iexp]]$v=as.double(mx[ijpwef[[iexp]][,1L]]*dpwe)
            mpf[]=meas2sum[[iexp]] %stm% dpw_dpf[[iexp]]
            # growth flux depending on free pools
            if (nbfgr > 0L) {
               bop(mpf, 1L, "+=", as.matrix(mffg[,nbff+seq_len(nbfgr),drop=FALSE]))
               mff=mffg[,seq_len(nbff)]
            } else {
               mff=mffg
            }
         }
         mff=as.matrix(mff)
         # store usefull information in global list jx_f
         bop(jx_f$dux_dp[[iexp]], c(2L, 0L, nbff), "=", mff)
         bop(jx_f$dux_dp[[iexp]], c(2L, nbff, nbl$poolf), "=", mpf)
         jx_f$param[]=param
         jx_f$x_f[[iexp]]=x_f
      }
   }
   jx_f$x=x
   return(list(x=jx_f$x, lf=jx_f$lf))
}

Tiso2cumo=function(len) {
   if (len<0L)
      return(FALSE)
   if (len==0L)
      return(matrix(1L,1L,1L))
   # recursive call for len>1
   T=Tiso2cumo(len-1L)
   return(rbind(cbind(T,T),cbind(diag(0,NROW(T)),T)))
}

Tcumo2iso=function(len) {
   if (len<0L) {
      return(FALSE)
   }
   if (len==0L) {
      return(matrix(1L,1L,1L))
   }
   # recursive call for len>1
   T=Tcumo2iso(len-1L)
   return(rbind(cbind(T,-T),cbind(diag(0L,NROW(T)),T)))
}

Tiso2mass=function(len) {
   mass=matrix(0L, len+1L, 2L**len)
   for (i in 0L:(2L**len-1L)) {
      s=sumbit(i)
      mass[s+1L,i+1L]=1L
   }
   return(mass)
}

Vcumo2iso0=function(len) {
   # coefficients of first row of matrix Tcumo2iso
   # giving the conversion to isotopomer of weight 0
   if (len<0L) {
      return(FALSE)
   }
   if (len==0L) {
      return(c(1L))
   }
   # recursive call for len>1
   V=Vcumo2iso0(len-1L)
   return(c(V,-V))
}

sumbit=function(i) {
   # return the sum of bits in every component of the integer vector i
   # The result has the length=length(i)
   return(as.integer(colSums(outer(2L**(0L:30L), as.integer(i), bitops::bitAnd) > 0L)))
}

cumo2mass=function(x, sep=":", emusep="+") {
   # convert cumomer or emu vector(s) to MID vector(s)
   # x may be multiple column matrix,
   # each of its column is then translated into MID column.
   # x names expected in format Metab:N, where N is an integer.
   # or Metab:N+m, where m is emu weight M+m .
   
   if (length(x)==0L) {
      return(NULL)
   }
   # prepare x as matrix
   nbexp=NA
   if (is.vector(x) && !is.list(x)) {
      nmx=names(x)
      x=as.matrix(x)
   } else if (is.matrix(x)) {
      nmx=rownames(x)
   } else if (is.list(x)) {
      nmx=rownames(x[[1L]])
      nbexp=length(x)
      nmexp=names(x)
   } else {
      stop("x is an unknown structure. It must be vector, matrix or a list of matrices")
   }
   
   # is it emu or cumomer vector
   emu=TRUE
   if (is.na(strsplit(nmx[1L], emusep, fixed=TRUE)[[1L]][2L])) {
      emu=FALSE
   }
   if (emu) {
      # just take the longest fragments and return their MID
      spl=data.frame(t(vapply(strsplit(nmx, "[" %s+% sep %s+% emusep %s+% "]"), c, character(3L))),
         stringsAsFactors=F)
      spl[,2L]=as.integer(spl[,2L])
      longest=tapply(spl[,2L], list(spl[,1L]), max)
      o=order(names(longest))
      longest=longest[o]
      nml=names(longest)
      # select the MIDs of the longest fragment
      if (is.na(nbexp)) {
         res=x[unlist(sapply(nml, function(nm) which(spl[,1L]==nm&spl[,2L]==longest[nm]))),,drop=FALSE]
      } else {
         i=unlist(sapply(nml, function(nm) which(spl[,1L]==nm&spl[,2L]==longest[nm])))
         res=lapply(x, function(xx) xx[i,,drop=FALSE])
      }
      return(res)
   }

   # separate cumos by name and order by weight
   metabs=c(); # unique metab names
   spl=as.matrix(sapply(nmx, function(s) {
      v=strsplit(s, sep, fixed=TRUE)[[1L]]
      if (length(v)==2L) {
         return(v)
      } else {
         # badly formed cumomer name
         return(c(NA, NA))
      }
   }))
   i=!is.na(spl[2L,])
   if (is.na(nbexp)) {
      x=x[i,,drop=FALSE]
   } else {
      x=lapply(x, "[", i,,drop=FALSE)
   }
   spl=spl[,i,drop=FALSE]
   n=if (is.na(nbexp)) nrow(x) else nrow(x[[1L]])
   i=seq_len(n)
   icumo=as.integer(spl[2L,])
   metabs=spl[1L,]
   umetabs=union(metabs, NULL)
   # extract, order and convert each metab vector
   if (is.na(nbexp)) {
      res=matrix(0., nrow=0L, ncol=ncol(x))
      for (metab in umetabs) {
         im=metabs==metab
         o=order(icumo[im])
         # ordered cumomer vector with #0==1 component
         vcumo=rbind(1,x[im,,drop=FALSE][o,,drop=FALSE])
         clen=log2(nrow(vcumo))
         # check that we have all components
         sb=sumbit(max(icumo[im]))
         if (!isTRUE(all.equal(sb, clen))) {
            next
         }
         # mass vector
         mass=as.matrix(Tiso2mass(clen)%*%(Tcumo2iso(clen)%*%vcumo))
         rownames(mass)=paste(metab, "+", 0:clen, sep="")
         res=rbind(res, mass)
      }
   } else {
      rres=lapply(seq_len(nbl$exp), function(iexp) matrix(0., nrow=0L, ncol=ncol(x[[iexp]])))
      names(rres)=names(x)
      for (iexp in seq_len(nbl$exp)) {
         res=rres[[iexp]]
         for (metab in umetabs) {
            im=metabs==metab
            o=order(icumo[im])
            # ordered cumomer vector with #0==1 component
            vcumo=rbind(1,x[[iexp]][im,,drop=FALSE][o,,drop=FALSE])
            clen=log2(nrow(vcumo))
            # check that we have all components
            sb=sumbit(max(icumo[im]))
            if (!isTRUE(all.equal(sb, clen))) {
               next
            }
            # mass vector
            mass=as.matrix(Tiso2mass(clen)%*%(Tcumo2iso(clen)%*%vcumo))
            rownames(mass)=paste(metab, "+", 0:clen, sep="")
            res=rbind(res, mass)
         }
         rres[[iexp]]=res
      }
      res=rres
   }
   return(res)
}

cumo2lab=function(x) {
   # converts cumomer vector to fraction of labeled isotopomer 1-i#0
   # separate cumos by name and order by weight
   x=as.matrix(x)
   n=nrow(x)
   nmx=rownames(x)
   if (is.null(nmx)) {
      return(NULL)
   }
   metabs=c(); # unique metab names
   spl=unlist(strsplit(nmx,":",fix=TRUE))
   i=1:n
   icumo=as.integer(spl[2*i])
   metabs=spl[2*i-1]
   umetabs=union(metabs, NULL)
   # extract, order and convert each metab vector
   res=c()
   for (metab in umetabs) {
      im=metabs==metab
      o=order(icumo[im])
      # ordered cumomer matrix with #0==1 component
      vcumo=rbind(1,x[im,,drop=FALSE][o,,drop=FALSE])
      clen=log2(nrow(vcumo))
      # labeled fraction
      lab=1-Vcumo2iso0(clen)%*%vcumo
      rownames(lab)=metab
      res=rbind(res, lab)
   }
   return(res)
}
cumo2iso=function(x) {
   # converts cumomer vector to isotopomer vector
   # separate cumos by name and order by weight
   x=as.matrix(x)
   n=nrow(x)
   nmx=rownames(x)
   if (is.null(nmx)) {
      return(NULL)
   }
   metabs=c(); # unique metab names
   spl=unlist(strsplit(nmx,":",fix=TRUE))
   i=seq_len(n)
   icumo=as.integer(spl[2L*i])
   metabs=spl[2L*i-1L]
   umetabs=union(metabs, NULL)
   # extract, order and convert each metab vector
   res=c()
   for (metab in umetabs) {
      im=metabs==metab
      o=order(icumo[im])
      # ordered cumomer matrix with #0==1 component
      vcumo=rbind(1.,x[im,,drop=FALSE][o,,drop=FALSE])
      clen=round(log2(nrow(vcumo)))
      # labeled fraction
      lab=Tcumo2iso(clen)%*%vcumo
      rownames(lab)=paste(metab, seq_len(2L**clen)-1L, sep=":")
      res=rbind(res, lab)
   }
   return(res)
}
cumo_gradj=function(param, labargs) {
   # calculate gradient of cost function for cumomer minimization probleme
   if (any(ina <- is.na(jx_f$res)))
      grad=2.*as.numeric(crossprod(jx_f$res[!ina], jx_f$jacobian[!ina,,drop=FALSE]))
   else
      grad=2.*as.numeric(crossprod(jx_f$res, jx_f$jacobian))
   return(grad)
}

# cost function for donlp2 solver
cumo_fn=function(p) {
   return(cumo_cost(p, labargs))
}

cumo_dfn=function(p) {
   return(cumo_gradj(p, labargs))
}

attr(cumo_fn, "gr")=cumo_dfn
#cumo_fn@gr=cumo_dfn
cumo_jacob=function(param, labargs) {
   # calculate jacobian dmeas_dparam and some annexe matrices
   # without applying invvar matrix
   # The result is in a returned list jx_f.

   for (nm in c("noscale", "nbl", "nml", "sc", "jx_f", "sfi")) 
      assign(nm, labargs[[nm]])
   if (is.null(jx_f$udr_dp))
      jx_f$udr_dp=structure(matrix(0., nbl$resid, nbl$param), dimnames=list(nml$resid, nml$par))
   if (!noscale)
      mn=matrix(0., nbl$resid, nbl$param) # sufficiently big, then resized
   base=0L
   for (iexp in seq_len(nbl$exp)) {
      bop(jx_f$udr_dp, c(1L, base, nbl$meas[[iexp]]), "=", jx_f$dux_dp[[iexp]])
      if (!noscale && nbl$sc[[iexp]]) {
         for (isc in seq_along(sc[[iexp]])) {
            # mn: jacobian transformed for scaling
            ir=sc[[iexp]][[isc]]
            resize(mn, c(length(ir), nbl$param))
            bop(mn, 1L, "=", jx_f$dux_dp[[iexp]][ir,,drop=FALSE])
            bop(mn, 1L, "*=", sfi[[iexp]][[isc]]) # /=sum(v)
            smn=colSums(mn)
            bop(mn, 1L, "-=", jx_f$simlab[[iexp]][ir] %o% smn) # -= v %o% smn
            jx_f$udr_dp[base+ir,]=mn
         }
      }
      base=base+nbl$meas[[iexp]]
   }
   bop(jx_f$udr_dp, c(1L, base, nbl$fmn), "=", labargs$dufm_dp)
   bop(jx_f$udr_dp, c(1L, base+nbl$fmn, nbl$poolm), "=", labargs$dupm_dp)
   return(NULL)
}

fwrv2Abr=function(fwrv, spAbr, incu, nmrcumo, getA=TRUE, getb=TRUE, emu=FALSE) {
   # calculate sparse A and b (in A*x=b where x is cumomer vector)
   # from fields of the list spAbr
   # return a list(A, b)
   # 2012-02-21 sokol
   #
   # update :
   # added emu parameter.
   # In emu mode b_pre_emu, ind_fbe, ind_xe1 and ind_xe2 are lists
   # in spAbr one term per m+i weght.
   # incu is inemu vector
   # nmrcumo is nmemu
   # when returns b, it is a matrix with as many columns as cumomer weight.
   # emu+mi for i=0L,N-1 N is the fragment weight can be calculated
   # from A*x=b.
   # emu+mN have to be calculated from 1-sum(lighter weights m+i)
   # 2012-07-16 sokol
   
   #nbc=spAbr$nbc # cumomer or fragment number (when emu==TRUE)
   #w=spAbr$w # cumomer weight
#cat("fwrv2Abr 1\n")
   nbc=spAbr$nbc
   if (nbc == 0L) {
      A=spAbr$a
      b=spAbr$b
      return(list(A=if (getA) A else NULL, b=if (getb) b else NULL))
   }
   if (getA) {
      ind_a=spAbr$ind_a
      if (!is.matrix(ind_a))
         ind_a=t(ind_a)
      spAbr$xmat$v <- fwrv[ind_a[,"indf"]]
      x <- col_sums(spAbr$xmat)
      x[spAbr$iadiag] <- -x[spAbr$iadiag]
      spAbr$a$set_mat_data(x)
   }
   
   # construct a complete b vector
   if (getb) {
      ind_b=if (emu) spAbr[["ind_b_emu"]] else spAbr[["ind_b"]]
      nprodx=ncol(ind_b)-2L-emu
      prodx=incu[c(ind_b[,2L+emu+seq_len(nprodx)])]
      dim(prodx)=c(nrow(ind_b), nprodx)
      spAbr$bmat$v=fwrv[ind_b[,"indf"]]*arrApply(prodx, 2L, "prod")
      spAbr$b$v=-col_sums(spAbr$bmat)
   }
   return(list(A=if (getA) spAbr$a else NULL, b=if (getb) spAbr$b else NULL))
}

fx2jr=function(fwrv, spAbr, nb, incu) {
   # calculate sparse j_rhs and b_x from fields of the list spAbr
   # according to conventions explained in comments
   # to python function netan2Abcumo_spr() generating spAbr
   # Return a list j_rhs, b_x
   # nb is a list of various numbers (cumomers, emus and so on)
   # 2012-02-22 sokol
   #
   # update: added emu approach
   # if emu then incu is inemu vector
   # 2012-07-18 sokol
   #
   # update: added vectorization for multiple incu vectors considered
   # as matrix columns (there are nco of them) . output is a matrix with dim
   # (nbx*nco, nbfwrv)
   # 2014-07-15 sokol
   # cannot work for fullsys as nb contains numbers for reduced system
   
   # we derivate a*x=b implicitly
   # a_f*x + a*x_f=b_f + b_xl*xl_f
#browser()
   nbc=spAbr$nbc
   if (nbc==0) # no system at this weight
      return(list(j_rhsw=NULL, b_x=NULL, j_rhswp=NULL, b_xp=NULL))
   emu=is.matrix(spAbr$ind_b_emu)
   nbfwrv=spAbr$nbfwrv
   nbcl=spAbr$nbcl
   w=spAbr$w
   nbxi=nb$xi
   
   # a_fx
   ind_a=spAbr$ind_a
   if (!is.matrix(ind_a))
      ind_a=t(ind_a)
   i=ind_a[,"ic0"]==ind_a[,"ir0"]
   incu=as.matrix(incu)
   nco=ncol(incu)
   nro=nrow(ind_a)
   emuw=ifelse(emu, w, 1L)
   nbxw=nbc*emuw
   # first a_fx creation for further updates (a_fx can be of many different sizes
   # depending on the time scheme for ODE and possible parallel experiments)
   nma_fx=as.character(nco)
   if (is.null(spAbr$a_fxx)) {
      # create auxiliary data for a_fx
      spAbr$a_fxx=list()
   }   
   if (is.null(spAbr$a_fxx[[nma_fx]])) {
#cat("build", nma_fx, "\n", file=fclog)
      l=new.env()
      l$nco=nco
      if (emu) {
         ia=(ind_a[,"ir0"]+1L)+rep((seq_len(w)-1L)*nbc, each=nro)
         ja=rep(ind_a[,"indf"], w)
      } else {
         ia=ind_a[,"ir0"]+1L
         ja=ind_a[,"indf"]
      }
      l$ineg=which(ind_a[,"ic0"]==ind_a[,"ir0"])
      ia=ia+rep((seq_len(nco)-1L)*(nbc*emuw), each=nro*emuw)
      ja=rep(ja, nco)
      nar=nbxw*nco # row number in a_fx, b_f, b_x
      iv1=ia+(ja-1)*nar
      o=order(iv1)
      l$oa_x=o
      iv1=iv1[o]
      lrep=lrepx=rle(iv1)
      lrepx$values=seq_along(lrep$values)
      l$xmat=simple_triplet_matrix(i=unlist(lapply(lrep$lengths, seq_len)),
         j=inverse.rle(lrepx), v=rep(1, length(iv1)))
      iu1=lrep$values
      i=as.integer((iu1-1)%%nar)+1L
      j=as.integer((iu1-1)%/%nar)+1L
      l$a_fx=simple_triplet_matrix(i=i, j=j, v=rep(1, length(i)), nrow=nar, ncol=nbfwrv)
      
      # prepare b_f auxiliaries
      ind_b=if(emu) spAbr$ind_b_emu else spAbr$ind_b
      nro=nrow(ind_b)
      ib=ind_b[,"irow"]+if(emu) nbc*(ind_b[,"iwe"]-1L) else 0L
      jb=ind_b[,"indf"]
      ib=ib+rep((seq_len(nco)-1L)*nbxw, each=nro)
      jb=rep(jb, nco)
      iv1=ib+(jb-1)*nar
      o=order(iv1)
      l$ob_f=o
      iv1=iv1[o]
      lrep=lrepx=rle(iv1)
      lrepx$values=seq_along(lrep$values)
      l$b_fmat=simple_triplet_matrix(i=unlist(lapply(lrep$lengths, seq_len)),
         j=inverse.rle(lrepx), v=rep(1, length(iv1)))
      iu1=lrep$values
      i=as.integer((iu1-1)%%nar)+1L
      j=as.integer((iu1-1)%/%nar)+1L
      l$b_f=simple_triplet_matrix(i=i, j=j, v=rep(1, length(i)), nrow=nar, ncol=nbfwrv)
      # cache ind and pos for (b_f-a_fx)
      l$bma_pos=if (l$b_f$nrow*l$b_f$ncol < 2251799813685248 && l$a_fx$nrow*l$a_fx$ncol < 2251799813685248) match(l$a_fx$i+l$a_fx$j*l$a_fx$nrow, l$b_f$i+l$b_f$j*l$b_f$nrow, nomatch=0L) else match_ij(l$a_fx$i, l$a_fx$j, l$b_f$i, l$b_f$j)
      l$bma_ind=which(l$bma_pos == 0L)
      
      # prepare b_x auxiliaries
      if (length(spAbr$ind_bx) > 0L) {
         ind_bx=if (emu) spAbr$ind_bx_emu else spAbr$ind_bx
         nro=nrow(ind_bx)
         ib=ind_bx[,"irow"]
         jb=ind_bx[,"ic1"]
         ib=ib+rep((seq_len(nco)-1L)*nbxw, each=nro)
         jb=rep(jb, nco)
         iv1=ib+(jb-1)*nar
         o=order(iv1)
         l$ob_x=o
         iv1=iv1[o]
         lrep=lrepx=rle(iv1)
         lrepx$values=seq_along(lrep$values)
         l$b_xmat=simple_triplet_matrix(i=unlist(lapply(lrep$lengths, seq_len)),
            j=inverse.rle(lrepx), v=rep(1, length(iv1)))
         iu1=lrep$values
         i=as.integer((iu1-1)%%nar)+1L
         j=as.integer((iu1-1)%/%nar)+1L
         l$b_x=simple_triplet_matrix(i=i, j=j, v=rep(1, length(i)), nrow=nar, ncol=nb$c_x[w])
      } else {
         l$b_x=simple_triplet_zero_matrix(nrow=nar, ncol=nb$c_x[w])
      }
      spAbr$a_fxx[[nma_fx]]=l
   }
   x=incu[(1L+nbxi+nb$c_x[w])+seq_len(nbxw),,drop=FALSE]
   aux=spAbr$a_fxx[[nma_fx]]
   if (emu) {
      redim(x, c(nbc, w, nco))
      tmp=x[ind_a[,"ic0"]+1L,,,drop=FALSE]
      tmp[aux$ineg,,]=-tmp[aux$ineg,,]
   } else {
      tmp=x[ind_a[,"ic0"]+1L,,drop=FALSE]
      tmp[aux$ineg,]=-tmp[aux$ineg,]
   }
#browser()
   aux$xmat$v[]=tmp[aux$oa_x]
   aux$a_fx$v[]=slam::col_sums(aux$xmat)
   a_fx=aux$a_fx
   
   # prepare b_f
   # NB emu: b is shorter than xw by the last M+N vector which is added as (1-sum(lighter weights))
   ind_b=if(emu) spAbr$ind_b_emu else spAbr$ind_b
   nprodx=ncol(ind_b)-2-emu
   prodx=incu[c(ind_b[,2+emu+seq_len(nprodx)]),]
   dim(prodx)=c(nrow(ind_b), nprodx, nco)
   aux$b_fmat$v[]=-arrApply(prodx, 2, "prod")[aux$ob_f]
   aux$b_f$v[]=slam::col_sums(aux$b_fmat)
   b_f=aux$b_f
   
   # prepare b_x
   if (length(spAbr$ind_bx) > 0L) {
      ind_bx=if (emu) spAbr$ind_bx_emu else spAbr$ind_bx
      nprodx=ncol(ind_bx)-3-emu
      if (nprodx >= 1) {
         prodx=incu[c(ind_bx[,3+emu+seq_len(nprodx)]),]
         dim(prodx)=c(nrow(ind_bx), nprodx, nco)
         aux$b_xmat$v[]=(-fwrv[ind_bx[,"indf"]]*arrApply(prodx, 2, "prod"))[aux$ob_x]
      } else {
         aux$b_xmat$v[]=(-fwrv[ind_bx[,"indf"]])[aux$ob_x]
      }
      aux$b_x$v[]=slam::col_sums(aux$b_xmat)
      b_x=aux$b_x
   } else {
      b_x=simple_triplet_zero_matrix(nrow=nbxw*nco, ncol=nb$c_x[w])
   }
#browser()
   j_rhsw=stm_pm(b_f, a_fx, "-", aux$bma_pos, aux$bma_ind)
   if (is.null(aux$o_j)) {
      o=order(j_rhsw$i+j_rhsw$nrow*j_rhsw$j)
      aux$o_j=o
   }
   o=aux$o_j
   j_rhsw$i[]=j_rhsw$i[o]
   j_rhsw$j[]=j_rhsw$j[o]
   j_rhsw$v[]=j_rhsw$v[o]
   return(list(j_rhsw=j_rhsw, b_x=b_x))
}

put_inside=function(param, ui, ci, tol_in=1.e-10, tol_out=1.e-7, tol_desc=1.e-3) {
   # put param inside of feasible domain delimited by u%*%param >= ci
   nmpar=names(param)
   mes=""
   ineq=as.numeric(ui%*%param)-ci
   if (all(ineq>tol_in)) {
      # nothing to do, already inside and well inside
      return(param)
   }
   dp=ldp(as.matrix(ui), -ineq)
   if (!is.null(dp)) {
      # get new active inequalities
      ineqd=as.numeric(ui%*%(param+dp))-ci
      # check that we are not too far outside
      if (any(ineqd < -tol_out)) {
         param=NA
         attr(param, "mes")="Inequality system is ill-conditioned. Failed to solve."
         attr(param, "err")=1
         return(param)
      }
      iact=ineqd<=tol_in
#print(ineqd[iact])
      # solve an ldp pb to find non decreasing direction
      # for active inequalities
      ma=ui[iact,,drop=FALSE]
      na=sum(iact)
      # find closest vector to c(1,1,...) making the direction increasing
      tma=tcrossprod(ma)
      bet=ldp(tma, tol_desc - apply(tma, 1L, sum))
      if (is.null(bet)) {
         param=param+dp
         attr(param, "mes")="Infeasible constraints for inside direction."
         attr(param, "err")=0
         return(param)
      }
      vn=crossprod(ma, 1.+bet)
      vn=vn/norm(vn)
      decr=(ui%*%vn)<0.
      alpha=((-ineqd)/(ui%*%vn))[decr]
      alpha=alpha[alpha>0]
      alpha=0.5*min(tol_desc, alpha)
      dpn=dp+alpha*vn
      # check that new dp is still inside
      if (any(ui%*%(param+dpn)-ci < 0.)) {
         attr(param, "err")=0 # just a warning
         attr(param, "mes")="Failed to put free parameters strictly inside of the feasible domain. They are left on the border."
         dpn=dp
      }
      names(param)=nmpar
      if (!is.null(mget("nbff", ifnotfound=list(NULL))[[1L]]) && nbff > 0L) {
         i=abs(dpn[seq_len(nbff)])>=tol_in
         if (any(i)) {
            tmp=cbind(param[1:nbff], param[1:nbff]+dpn[1:nbff], dpn[1:nbff])
            dimnames(tmp)=list(nmpar[1:nbff], c("outside", "inside", "delta"))
            obj2kvh(tmp[i,,drop=FALSE], "Free fluxes put inside of feasible domain")
         }
      }
      # move starting point slightly inside of feasible domain
      param=param+as.numeric(dpn)
   } else {
      param=NA
      mes="Infeasible inequalities."
      if (!is.null(rownames(ui))) {
         mes=join("\n", c(mes, rownames(ui)))
      }
      attr(param, "mes")=mes
      attr(param, "err")=1
   }
   return(param)
}

df_dffp=function(param, flnx, nbl, nml) {
   # derivation of fwrv by free_fluxes+poolf (and not growth fluxes neither log(poolf))
   ah=1.e-10; # a heavyside parameter to make it derivable in [-ah; ah]
   nbfwrv=nbl$fwrv
   nmpar=names(param)
   i_fln=grep("d.n.", names(flnx), fixed=TRUE)
   i_flx=grep("d.x.", names(flnx), fixed=TRUE)
   i_ffn=grep("f.n.", nmpar, fixed=TRUE)
   i_ffx=grep("f.x.", nmpar, fixed=TRUE)
   if (nbl$fgr > 0L) {
      i_fgn=grep("pf:", nmpar, fixed=TRUE)
   } else {
      i_fgn=c()
   }
   i_fgx=c(); #grep("g.x.", nmpar, fixed=TRUE) # must be always empty
   nbff=length(i_ffn)+length(i_ffx)
   nbfgr=length(i_fgn)+length(i_fgx)
   #df_dfl=Matrix(0., nbfwrv, length(flnx))
   #df_dffd=Matrix(0., nbfwrv, nbff+nbfgr)
   df_dfl=simple_triplet_zero_matrix(nbfwrv, length(flnx))
   df_dffd=simple_triplet_zero_matrix(nbfwrv, nbff+nbfgr)
   # derivation by dependent fluxes
   # net part
   net=flnx[i_fln]
   hnet=Heaviside(net)
   i=abs(net)<ah
   hnet[i]=net[i]/ah
   # xch part
   xch=flnx[i_flx]
   xch=1./(1.-xch)**2
   
   # forward fluxes
   df_dfl[nbl$cfw_fl]=c(hnet, xch)
   # reverse fluxes
   df_dfl[nbl$crv_fl]=c(hnet-1., xch)
   
   # derivation by free fluxes
   # net part
   net=param[i_ffn]
   hnet=Heaviside(net)
   i=abs(net)<ah
   hnet[i]=net[i]/ah
   # xch part
   xch=param[i_ffx]
   xch=1./(1.-xch)**2
   # forward fluxes
   if (length(nbl$cfw_ff) > 0L)
      df_dffd[nbl$cfw_ff]=c(hnet, xch)
   # reverse fluxes
   if (length(nbl$crv_ff) > 0L)
      df_dffd[nbl$crv_ff]=c(hnet-1., xch)
   
   # derivation by growth fluxes
   # forward fluxes
   if (length(nbl$cfw_fg) > 0L)
      df_dffd[nbl$cfw_fg]=rep.int(1., length(i_fgn))
   # reverse fluxes
   if (length(nbl$crv_fg) > 0L)
      df_dffd[nbl$crv_fg]=0.
   
   res=df_dfl %stm% nbl$dfl_dffg+df_dffd
   if (nbfgr > 0L) {
      i=res$j > nbff
      res$v[i]=res$v[i]*nbl$mu
   }
   dimnames(res)=list(nml$fwrv, names(param)[c(i_ffn, i_ffx, i_fgn, i_fgx)])
   o=order(res$i+res$nrow*res$j)
   res$i[]=res$i[o]
   res$j[]=res$j[o]
   res$v[]=res$v[o]
   return(res)
}

dufm_dff=function(nbl, nml) {
   # measured fluxes derivation (non reduced by SD)
   res=matrix(0., length(nml$fmn), length(nml$ff))
   dimnames(res)=list(nml$fmn, nml$ff)
   # derivate free measured fluxes (trivial)
   i=grep("f.n.", nml$fmn, fixed=TRUE)
   if (length(i) > 0L) {
      res[i,nml$fmn[i]]=diag(length(i))
   }
   # derivate dependent measured fluxes
   i=grep("d.n.", nml$fmn, fixed=T, value=TRUE)
   if (length(i) > 0L) {
      res[i,]=as.matrix(nbl$dfl_dffg[i,1:length(nml$ff)])
   }
   return(res)
}

plot_ti=function(ti, x, m=NULL, ...) {
   # plot time curse curves x[icurve, itime] and points from m
   # x and m are supposed to have the same dimension and organization
   nm=rownames(x)
   nbcurve=nrow(x)
   if (is.null(nm)) {
      nm=seq_len(nbcurve)
   } else {
      o=order(nm)
      nm=nm[o]
      x=x[o,,drop=FALSE]
      if (!is.null(m) && nrow(x)==nrow(m)) {
         m=m[o,,drop=FALSE]
      }
   }
   # x and m may have different time moments
   if (is.null(m)) {
      tim=ti
      inna=c()
   } else {
      tim=as.numeric(colnames(m))
      inna=which(!is.na(m))
   }
   plot(range(ti, tim), range(c(x,m[inna])), t="n", ylab="Labeling", xlab="Time", ...)
   matplot(ti, t(x), t="l", lty=1:nbcurve, col=1:nbcurve, lwd=2, add=TRUE)
   legend("topright", legend=nm, lty=1:nbcurve, col=1:nbcurve, lwd=2, cex=0.75)
   if (!is.null(m)) {
      # plot measured points
      for (i in 1:nrow(m)) {
         inna=which(!is.na(m[i,]))
         points(tim[inna], m[i,inna], col=i, cex=0.5, t="b", lwd=0.5)
         if (nrow(m) == nbcurve) {
            # draw filled polygons between simulation and data
            polygon(c(ti,rev(tim[inna])), c(x[i,], rev(m[i,inna])), col=rgb(red=t(col2rgb(i)), alpha=31, max=255), bord=F)
         }
      }
   }
}

get_usm=function(f) {
   # return list of ti, usm from a _res.kvh file f

   # get skip and end number in the kvh
   d=kvh_get_matrix(f, c("simulated unscaled labeling measurements"))
   ti=as.numeric(colnames(d))
   o=order(rownames(d))
   return(list(ti=ti, usm=d[o,,drop=FALSE]))
}

get_labcin=function(f, nmmeas=NULL) {
   # get labeling cinetic data form file f
   # with rows matching at the best nmmeas (if any)
   d=as.matrix(read.table(f, header=TTRUE, row.names=1L, sep="\t", check=F, comment=""))
   # strip the last field (row id) in nmmeas and make it correspond
   # to rownames of d
   if (is.null(nmmeas)) {
      return(d)
   }
   nmr=rownames(d)
   nm=sapply(nmmeas, function(s) {
      v=strsplit(s, ":", fixed=TRUE)[[1L]]
      v[length(v)]=""
      pmatch(paste(v, sep=":", collapse=":"), nmr)
   })
   nm=nm[!is.na(nm)]
   return(d[nm,])
}

get_hist=function(f, v) {
   # matrix from history field from a _res.kvh file f

   # get skip and end number in the kvh
   d=kvh_get_matrix(f, c("history", v))
   return(d)
}

opt_wrapper=function(param, method, measurements, jx_f, labargs, trace=1) {
   oldmeas=labargs$measurements
   labargs$measurements=measurements
   labargs$jx_f=jx_f
   if (method == "BFGS") {
#browser()
      control=list(maxit=500L, trace=trace)
      control[names(control_ftbl$BFGS)]=control_ftbl$BFGS
      res=constrOptim(param, cumo_cost, grad=cumo_gradj,
         ui, ci, mu = 1e-5, control,
         method="BFGS", outer.iterations=100L, outer.eps=1e-08,
         labargs)
   } else if (method == "Nelder-Mead") {
      control=list(maxit=1000L, trace=trace)
      control[names(control_ftbl[["Nelder-Mead"]])]=control_ftbl[["Nelder-Mead"]]
      res=constrOptim(param, cumo_cost, grad=cumo_gradj,
         ui, ci, mu = 1e-4, control,
         method="Nelder-Mead", outer.iterations=100, outer.eps=1e-08,
         labargs)
   } else if (method == "SANN") {
      control=list(maxit=1000L, trace=trace)
      control[names(control_ftbl$sann)]=control_ftbl$sann
      res=constrOptim(param, cumo_cost, grad=cumo_gradj,
         ui, ci, mu = 1e-4, control,
         method="SANN", outer.iterations=100L, outer.eps=1e-08,
         labargs)
   } else if (method == "nlsic") {
      control=list(trace=trace, btfrac=0.25, btdesc=0.1, maxit=50L, errx=1.e-5,
         ci=list(report=F), history=FALSE, adaptbt=TRUE, sln=sln,
         maxstep=max(10.*sqrt(norm2(param)), 1.)
      )
      control[names(control_ftbl$default)]=control_ftbl$default
      control[names(control_ftbl$nlsic)]=control_ftbl$nlsic
      res=nlsic(param, labargs$lab_resid, 
         labargs$ui, labargs$ci, control, e=labargs$ep, eco=labargs$cp, flsi=labargs$lsi_fun,
         labargs)
   } else if (method == "ipopt") {
      control=list(max_iter=500L, print_level=trace*5L)
      control[names(control_ftbl$ipopt)]=control_ftbl$ipopt
      tui=c(t(ui))
      eval_g=function(x, labargs) {
         return(ui%*%x)
      }
      eval_jac_g=function(x, labargs) {
         return(tui)
      }
      ui_row_spars=rep.int(1, ncol(ui))
      res=ipoptr(param, cumo_cost, cumo_gradj,
         lb=NULL, ub=NULL,
         eval_g=eval_g,
         eval_jac_g=eval_jac_g,
         eval_jac_g_structure=lapply(1L:nrow(ui), function(i)ui_row_spars),
         constraint_lb=ci,
         constraint_ub=rep(1.e19, length(ci)),
         eval_h=NULL,
         eval_h_structure=NULL,
         opts=control,
         ipoptr_environment=new.env(),
         labargs)
      res$par=res$solution
      names(res$par)=nmpar
   } else if (method == "pso") {
      control=list(
         type="SPSO2011",
         trace=trace,
         maxit=100L,
         reltol=1.e-2
      )
      control[names(control_ftbl$pso)]=control_ftbl$pso
#print(control_ftbl)
#print(control)
      res=try(psoptim_ic(param, cumo_cost, labargs, mean=0.5, control=control, ui=ui, ci=ci), silent=TRUE)
#print(res)
      if (inherits(res, "try-error")) {
         res=list(err=1L, par=NULL, mes=attr(res, "condition")$message)
      } else {
         tmp=list(err=res$msgcode, par=res$par, mes=res$msg)
         res[c("msg", "par", "msg")]=NULL
         res=c(tmp, res) # preserve the rest of the fields: stats etc.
      }
   } else {
      stop_mes("Unknown minimization method '", method, "'", file=fcerr)
   }
   if (is.null(res$err)) {
      res$err=0L
   }
   labargs$measurements=oldmeas
   return(res)
}

# wrapper for Monte-Carlo simulations
mc_sim=function(imc) {
   labargs=get("labargs", envir=.GlobalEnv)
   for (item in c("nbl", "measurements", "case_i", "dirres", "baseshort", "nbexp")) {
      assign(item, labargs[[item]])
   }
   # random measurement generation
   if (case_i) {
      meas_mc=lapply(seq_len(nbexp), function(iexp) if (nbl$meas[iexp]) refsim$usm[[iexp]]+rnorm(n=length(refsim$usm[[iexp]]))*measurements$dev$labeled[[iexp]] else NULL)
   } else {
      meas_mc=lapply(seq_len(nbexp), function(iexp) if (nbl$meas[iexp]) refsim$simlab[[iexp]]+rnorm(n=length(refsim$simlab[[iexp]]))*measurements$dev$labeled[[iexp]] else NULL)
   }
   if (nbl$fmn) {
      fmn_mc=refsim$simfmn+rnorm(n=length(refsim$simfmn))*measurements$dev$flux
   } else {
      fmn_mc=c()
   }
   if (nbl$poolm) {
      poolm_mc=refsim$simpool+rnorm(n=length(refsim$simpool))*measurements$dev$pool
   } else {
      poolm_mc=c()
   }
   # minimization
   measurements_mc=measurements
   if (case_i) {
      measurements_mc$vec$kin=meas_mc
   } else {
      measurements_mc$vec$labeled=meas_mc
   }
   measurements_mc$vec$flux=fmn_mc
   measurements_mc$vec$pool=poolm_mc
   loc_jx_f=new.env()
   res=opt_wrapper(param, tail(methods, 1L), measurements_mc, loc_jx_f, labargs, trace=0L)
   if (res$err && !is.null(res$mes) && nchar(res$mes) > 0L) {
      fclog=file(file.path(dirres, "tmp", sprintf("%s.%smc%d.log", baseshort, runsuf, imc)), "wb")
      cat((if (res$err) "***Error" else "***Warning"), " in Monte-Carlo i=", imc, ": ", res$mes, "\n", file=fclog, sep="")
      close(fclog)
      if (res$err) {
         res=list(cost=NA, it=res$it, normp=res$normp, par=res$par, err=res$err)
         rm(loc_jx_f)
         gc()
         return(list(cost=NA, it=res$it, normp=res$normp, par=res$par, err=res$err))
      }
   }
   # return the solution
   iva=!is.na(res$res)
   vres=res$res[iva]
   res=list(cost=crossprod(vres)[1L], it=res$it, normp=res$normp, par=res$par, err=res$err)
   rm(loc_jx_f)
   gc() # for big problems we run easily out of memory
   return(res)
}
cl_worker=function(funth=NULL, argth=NULL) {
   if ("labargs" %in% names(argth))
      labargs=argth$labargs
   tryCatch({
      do.call(funth, argth)
   },
   error=function(e) {
      traceback()
      print(e)
      stop(e)
   })
}

fallnx2fwrv=function(fallnx, nbl) {
   n=length(fallnx)
   # extract and reorder in fwrv order
   net=fallnx[nbl$inet2ifwrv]
   xch=fallnx[nbl$ixch2ifwrv]
   # expansion 0;1 -> 0;+inf of xch (second half of fallnx)
   xch=xch/(1-xch)
   fwrv=c(xch-pmin(-net,0),xch-pmin(net,0))
   return(fwrv)
}
stm_pm=function(e1, e2, pm=c("+", "-"), pos=if (e1$nrow*e1$ncol < 2251799813685248 && e2$nrow*e2$ncol < 2251799813685248) match(e2$i+e2$j*e2$nrow, e1$i+e1$j*e1$nrow, nomatch=0L) else match_ij(e2$i, e2$j, e1$i, e1$j), ind=which(pos == 0L)) {
   # 2**51 is the max matrix size that fits the length of double mantissa (53 bits))
   if (pm == "+") {
      e1$v[pos] = e1$v[pos] + e2$v[pos > 0L]
      e1$v = c(e1$v, e2$v[ind])
   } else {
      e1$v[pos] = e1$v[pos] - e2$v[pos > 0L]
      e1$v = c(e1$v, -e2$v[ind])
   }
   e1$i = c(e1$i, e2$i[ind])
   e1$j = c(e1$j, e2$j[ind])
   return(e1)
}
`%m+%`=function(m, n) outer(if (is.array(m)) m else seq(0, m), seq(0, n), "+")
